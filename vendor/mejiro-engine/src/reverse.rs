//! Desktop reverse lookup. Firmware builds do not enable the `reverse` feature.
//! Candidate strokes are always checked with the forward translator, including
//! runtime dictionary overlays and state carried across strokes.
use crate::tables::{
    ABSTRACT_MAP, ABSTRACT_MAP_LEFT, ABSTRACT_MAP_RIGHT, CONSONANTS, EXCEPTION_KANA,
    MINOR_DIPHTHONGS, PARTICLE_KEY_LIST, VERB_MAP,
};
use crate::{Request, RuleKind, RuleStore, State, Stroke, translate_with_rules};
use std::collections::BTreeSet;
use std::string::{String, ToString};
use std::vec::Vec;

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum Kind {
    Particle,
    Verb,
    General,
    User,
    Minor,
    Basic,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Segment {
    /// Character offsets in the requested hiragana string, end-exclusive.
    pub start: usize,
    pub end: usize,
    pub kind: Kind,
    /// Dictionary form for a verb, if the forward translator can resolve it.
    pub lemma: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Candidate {
    pub strokes: String,
    pub segments: Vec<Segment>,
    pub stroke_count: usize,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GrammarSpan {
    pub start: usize,
    pub end: usize,
    pub kind: Kind,
    pub lemma: Option<String>,
}

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct ReverseResult {
    pub all: Vec<Candidate>,
    pub basic_and_particle: Vec<Candidate>,
    pub truncated: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ReverseError {
    InputTooLong,
    SearchLimit,
}

const MAX_RESULTS: usize = 10;
const MAX_CHARS: usize = 32;
const MAX_VISITS: usize = 500_000;

/// Return at most ten candidates for each route. `grammar` is optional and
/// influences order only; mismatches are retained. An unrepresentable basic
/// route means neither route has a bounded search and both lists are empty.
pub fn lookup(
    text: &str,
    grammar: &[GrammarSpan],
    rules: &RuleStore,
) -> Result<ReverseResult, ReverseError> {
    if text.chars().count() > MAX_CHARS {
        return Err(ReverseError::InputTooLong);
    }
    if text.is_empty() || !text.chars().all(is_hiragana) {
        return Ok(ReverseResult::default());
    }
    let seeds = seeds(text, rules);
    let (mut basic, basic_truncated) = search(text, grammar, rules, &seeds, true, MAX_CHARS);
    let Some(bound) = basic.iter().map(|c| c.stroke_count).min() else {
        return if basic_truncated {
            Err(ReverseError::SearchLimit)
        } else {
            Ok(ReverseResult::default())
        };
    };
    let (all, all_truncated) = search(text, grammar, rules, &seeds, false, bound);
    basic.truncate(MAX_RESULTS);
    Ok(ReverseResult {
        all,
        basic_and_particle: basic,
        truncated: basic_truncated || all_truncated,
    })
}

fn is_hiragana(c: char) -> bool {
    ('\u{3041}'..='\u{3096}').contains(&c) || matches!(c, 'ー' | '・' | '、' | '。' | '？')
}

fn hand_parts() -> Vec<String> {
    let mut out = Vec::new();
    for (c, _) in CONSONANTS {
        for v in [
            "", "A", "I", "U", "IA", "AU", "YA", "YU", "YAU", "Y", "YI", "YIA", "YIU", "YIAU",
            "IU", "IAU",
        ] {
            for p in PARTICLE_KEY_LIST {
                out.push(std::format!("{c}{v}{p}"));
            }
        }
    }
    out
}

fn seeds(target: &str, rules: &RuleStore) -> Vec<(String, Kind)> {
    let parts = hand_parts();
    let mut raw = BTreeSet::new();
    for l in &parts {
        if !l.is_empty() {
            raw.insert(std::format!("{l}-"));
        }
    }
    for r in &parts {
        if !r.is_empty() {
            raw.insert(std::format!("-{r}"));
        }
    }
    // Independent particles and the right-hand ordinary kana need no prefix.
    // STN has no kana of its own, so it probes right-hand phonetic fragments.
    let relevant_left: Vec<&String> = parts
        .iter()
        .filter(|p| {
            if p.is_empty() {
                return true;
            }
            let probe = std::format!("{p}-");
            match translate_with_rules(&probe, State::default(), false, rules) {
                Ok(t) => {
                    t.output.operations().is_empty()
                        && (t.output.text.as_str().is_empty()
                            || target.contains(t.output.text.as_str()))
                }
                Err(_) => false,
            }
        })
        .collect();
    let relevant_right: Vec<&String> = parts
        .iter()
        .filter(|p| {
            if p.is_empty() {
                return true;
            }
            let probe = std::format!("STN-{p}");
            match translate_with_rules(&probe, State::default(), false, rules) {
                Ok(t) => {
                    t.output.operations().is_empty()
                        && (t.output.text.as_str().is_empty()
                            || target.contains(t.output.text.as_str()))
                }
                Err(_) => false,
            }
        })
        .collect();
    for l in &relevant_left {
        for r in &relevant_right {
            if l.is_empty() && r.is_empty() {
                continue;
            }
            raw.insert(std::format!("{l}-{r}"));
            raw.insert(std::format!("{l}-{r}*"));
        }
    }
    // Verb inflections are not compositionally related to the two syllables.
    // Restrict their left side to possible prefixes, then test every ending.
    for l in &relevant_left {
        let probe = std::format!("{l}-");
        let Ok(parsed) = Stroke::parse(&probe) else {
            continue;
        };
        if !parsed.left.particle.is_empty() {
            continue;
        }
        for (c, _) in CONSONANTS {
            for v in ["", "I", "IA", "IU"] {
                for lp in PARTICLE_KEY_LIST {
                    for rp in PARTICLE_KEY_LIST {
                        let left =
                            std::format!("{}{}{lp}", parsed.left.consonant, parsed.left.vowel);
                        raw.insert(std::format!("{left}-{c}{v}{rp}"));
                        raw.insert(std::format!("{left}-{c}{v}{rp}*"));
                    }
                }
            }
        }
    }
    // Built-in and edited dictionary keys can replace otherwise unrelated
    // kana, so include their inflected/particle variants explicitly.
    for key in ABSTRACT_MAP
        .iter()
        .map(|(k, _)| *k)
        .chain(VERB_MAP.iter().map(|(k, _)| *k))
        .chain(
            rules
                .entries()
                .iter()
                .filter(|e| matches!(e.kind, RuleKind::General | RuleKind::Verb | RuleKind::User))
                .map(|e| e.key.as_str()),
        )
    {
        if key.ends_with('*') {
            raw.insert(key.to_string());
            continue;
        }
        raw.insert(key.to_string());
        if let Some((l, r)) = key.split_once('-') {
            for lp in PARTICLE_KEY_LIST {
                for rp in PARTICLE_KEY_LIST {
                    raw.insert(std::format!("{l}{lp}-{r}{rp}"));
                    raw.insert(std::format!("{l}{lp}-{r}{rp}*"));
                }
            }
        }
    }
    let left_keys: BTreeSet<&str> = ABSTRACT_MAP_LEFT
        .iter()
        .map(|(key, _)| *key)
        .chain(
            rules
                .entries()
                .iter()
                .filter(|e| e.kind == RuleKind::GeneralLeft)
                .map(|e| e.key.as_str()),
        )
        .collect();
    let right_keys: BTreeSet<&str> = ABSTRACT_MAP_RIGHT
        .iter()
        .map(|(key, _)| *key)
        .chain(
            rules
                .entries()
                .iter()
                .filter(|e| e.kind == RuleKind::GeneralRight)
                .map(|e| e.key.as_str()),
        )
        .collect();
    for left in left_keys {
        for right in &right_keys {
            raw.insert(std::format!("{left}-{right}*"));
        }
    }
    let mut candidates: Vec<(String, Kind)> = raw
        .into_iter()
        .filter_map(|key| {
            let t = translate_with_rules(&key, State::default(), false, rules).ok()?;
            let body = t.output.text.as_str();
            let dependent = Stroke::parse(&key).ok().is_some_and(|s| {
                let left_only = s.right.consonant.is_empty()
                    && s.right.vowel.is_empty()
                    && s.right.particle.is_empty();
                let right_only = s.left.consonant.is_empty()
                    && s.left.vowel.is_empty()
                    && s.left.particle.is_empty();
                !s.star
                    && (left_only && !s.left.consonant.is_empty() && s.left.vowel.is_empty()
                        || right_only && !s.right.consonant.is_empty() && s.right.vowel.is_empty()
                        || s.left.consonant.is_empty()
                            && s.left.vowel.is_empty()
                            && s.right.consonant.is_empty()
                            && s.right.vowel.is_empty())
            });
            if t.request != Request::Output
                || !t.output.operations().is_empty()
                || body.is_empty() && !dependent
                || !target.contains(body) && !dependent
            {
                return None;
            }
            Some((key.clone(), classify(&key, rules)))
        })
        .collect();
    // The hash key repeats ordinary kana in one stroke. Add it only when the
    // repeated text occurs in the query, so it cannot crowd unrelated output.
    let mut repeated = Vec::new();
    for (key, kind) in &candidates {
        if key.starts_with('#') {
            continue;
        }
        let Ok(t) = translate_with_rules(key, State::default(), false, rules) else {
            continue;
        };
        let body = t.output.text.as_str();
        if body.is_empty() || !target.contains(&std::format!("{body}{body}")) {
            continue;
        }
        let doubled = std::format!("#{key}");
        if let Ok(t) = translate_with_rules(&doubled, State::default(), false, rules)
            && t.request == Request::Output
            && t.output.operations().is_empty()
            && target.contains(t.output.text.as_str())
        {
            repeated.push((doubled, *kind));
        }
    }
    candidates.extend(repeated);
    candidates.sort_by(|a, b| a.0.cmp(&b.0));
    candidates
}

fn classify(raw: &str, rules: &RuleStore) -> Kind {
    if rules.find(RuleKind::User, raw).is_some_and(|e| !e.hidden) {
        return Kind::User;
    }
    let Ok(s) = Stroke::parse(raw) else {
        return Kind::Basic;
    };
    let l = s.left;
    let r = s.right;
    if l.consonant.is_empty() && l.vowel.is_empty() && r.consonant.is_empty() && r.vowel.is_empty()
    {
        return Kind::Particle;
    }
    let key = std::format!("{}{}-{}{}", l.consonant, l.vowel, r.consonant, r.vowel);
    let full = std::format!("{key}{}", if s.star { "*" } else { "" });
    let direct = rules
        .find(RuleKind::General, &full)
        .map(|e| !e.hidden)
        .unwrap_or_else(|| ABSTRACT_MAP.iter().any(|(k, _)| *k == full));
    let lk = std::format!("{}{}", l.consonant, l.vowel);
    let rk = std::format!("{}{}", r.consonant, r.vowel);
    let left_general = rules
        .find(RuleKind::GeneralLeft, &lk)
        .map(|e| !e.hidden)
        .unwrap_or_else(|| ABSTRACT_MAP_LEFT.iter().any(|(k, _)| *k == lk));
    let right_general = rules
        .find(RuleKind::GeneralRight, &rk)
        .map(|e| !e.hidden)
        .unwrap_or_else(|| ABSTRACT_MAP_RIGHT.iter().any(|(k, _)| *k == rk));
    if direct || s.star && left_general && right_general {
        return Kind::General;
    }
    if r.consonant == "TN" && r.vowel.is_empty()
        || matches!(key.as_str(), "I-K" | "A-ST" | "K-")
        || !r.consonant.is_empty() && r.vowel.is_empty() && !matches!(r.consonant, "STN")
        || s.star
            && (VERB_MAP.iter().any(|(k, _)| *k == key)
                || rules.find(RuleKind::Verb, &key).is_some_and(|e| !e.hidden))
    {
        return Kind::Verb;
    }
    let exceptional = [l, r].iter().any(|h| {
        let cv = std::format!("{}{}", h.consonant, h.vowel);
        let minor = std::format!("{}{}", h.vowel, h.particle);
        EXCEPTION_KANA.iter().any(|(k, _)| *k == cv)
            || MINOR_DIPHTHONGS.iter().any(|(k, _)| *k == minor)
            || matches!(h.vowel, "Y" | "YI" | "YIA" | "YIU" | "YIAU" | "IU" | "IAU")
    });
    if exceptional {
        return Kind::Minor;
    }
    Kind::Basic
}

fn output_segments(
    raw: &str,
    kind: Kind,
    body: &str,
    state: State,
    rules: &RuleStore,
    start: usize,
) -> Vec<Segment> {
    let end = start + body.chars().count();
    if matches!(kind, Kind::Particle | Kind::User) {
        return std::vec![Segment {
            start,
            end,
            kind,
            lemma: None
        }];
    }
    let mut lemma = None;
    if let Ok(stroke) = Stroke::parse(raw)
        && (!stroke.left.particle.is_empty() || !stroke.right.particle.is_empty())
    {
        let plain = std::format!(
            "{}{}-{}{}{}",
            stroke.left.consonant,
            stroke.left.vowel,
            stroke.right.consonant,
            stroke.right.vowel,
            if stroke.star { "*" } else { "" }
        );
        if let Ok(t) = translate_with_rules(&plain, state, false, rules) {
            let base = t.output.text.as_str();
            if kind == Kind::Verb && !base.is_empty() {
                lemma = Some(base.to_string());
            }
            if !base.is_empty() && body.starts_with(base) && base.len() < body.len() {
                let middle = start + base.chars().count();
                return std::vec![
                    Segment {
                        start,
                        end: middle,
                        kind,
                        lemma
                    },
                    Segment {
                        start: middle,
                        end,
                        kind: Kind::Particle,
                        lemma: None
                    }
                ];
            }
        }
    }
    std::vec![Segment {
        start,
        end,
        kind,
        lemma
    }]
}

fn search(
    text: &str,
    grammar: &[GrammarSpan],
    rules: &RuleStore,
    seeds: &[(String, Kind)],
    basic_only: bool,
    max_depth: usize,
) -> (Vec<Candidate>, bool) {
    let mut found = Vec::new();
    let mut truncated = false;
    let mut path = Vec::new();
    let mut segments = Vec::new();
    #[allow(clippy::too_many_arguments)]
    fn walk(
        text: &str,
        offset: usize,
        state: State,
        depth: usize,
        max_depth: usize,
        seeds: &[(String, Kind)],
        rules: &RuleStore,
        basic_only: bool,
        path: &mut Vec<String>,
        segments: &mut Vec<Segment>,
        found: &mut Vec<Candidate>,
        visits: &mut usize,
    ) {
        if *visits >= MAX_VISITS || found.len() >= 10_000 {
            return;
        }
        if offset == text.len() {
            if !state.pending_sokuon() {
                found.push(Candidate {
                    strokes: path.join("/"),
                    segments: segments.clone(),
                    stroke_count: path.len(),
                });
            }
            return;
        }
        if depth == max_depth {
            return;
        }
        for (raw, kind) in seeds {
            if basic_only && !matches!(kind, Kind::Basic | Kind::Particle) {
                continue;
            }
            *visits += 1;
            if *visits >= MAX_VISITS {
                break;
            }
            let Ok(t) = translate_with_rules(raw, state, false, rules) else {
                continue;
            };
            let body = t.output.text.as_str();
            if t.request != Request::Output
                || !t.output.operations().is_empty()
                || body.is_empty()
                || !text[offset..].starts_with(body)
            {
                continue;
            }
            let start = text[..offset].chars().count();
            path.push(raw.clone());
            let parts = output_segments(raw, *kind, body, state, rules, start);
            segments.extend(parts.iter().cloned());
            walk(
                text,
                offset + body.len(),
                t.next,
                depth + 1,
                max_depth,
                seeds,
                rules,
                basic_only,
                path,
                segments,
                found,
                visits,
            );
            for _ in 0..parts.len() {
                segments.pop();
            }
            path.pop();
        }
    }
    // Iterative deepening enforces shortest stroke count before any category
    // preference, and stops once enough alternatives have been collected.
    for depth in 1..=max_depth {
        let mut visits = 0;
        walk(
            text,
            0,
            State::default(),
            0,
            depth,
            seeds,
            rules,
            basic_only,
            &mut path,
            &mut segments,
            &mut found,
            &mut visits,
        );
        truncated |= visits >= MAX_VISITS || found.len() >= 10_000;
        if basic_only && !found.is_empty() {
            break;
        }
        if found.len() >= 10_000 {
            break;
        }
    }
    found.sort_by(|a, b| {
        let score = |c: &Candidate| -> (usize, usize, usize, usize, String) {
            let mismatch = grammar
                .iter()
                .filter(|g| {
                    !c.segments.iter().any(|s| {
                        s.kind == g.kind
                            && s.start == g.start
                            && s.end == g.end
                            && g.lemma
                                .as_ref()
                                .is_none_or(|lemma| s.lemma.as_ref() == Some(lemma))
                    })
                })
                .count();
            let plain = c
                .segments
                .iter()
                .filter(|s| matches!(s.kind, Kind::Basic | Kind::Minor))
                .count();
            let decoration = c
                .strokes
                .bytes()
                .filter(|b| matches!(b, b'*' | b'#'))
                .count();
            if basic_only {
                (
                    c.stroke_count,
                    mismatch,
                    plain,
                    decoration,
                    c.strokes.clone(),
                )
            } else {
                (
                    mismatch,
                    c.stroke_count,
                    plain,
                    decoration,
                    c.strokes.clone(),
                )
            }
        };
        score(a).cmp(&score(b))
    });
    found.dedup_by(|a, b| a.strokes == b.strokes);
    found.truncate(MAX_RESULTS);
    (found, truncated)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn itte_has_verb_and_basic_candidates() {
        let result = lookup("いって", &[], &RuleStore::new()).unwrap();
        assert!(
            result.all.iter().any(|c| c.strokes == "I-SKntk"),
            "{:?}",
            result.all
        );
        assert!(
            result
                .basic_and_particle
                .iter()
                .any(|c| c.strokes == "Itk-TIA"),
            "{:?}",
            result.basic_and_particle
        );
    }
    #[test]
    fn to_wa_itte_mo_keeps_two_routes() {
        let result = lookup(
            "とはいっても",
            &[GrammarSpan {
                start: 2,
                end: 5,
                kind: Kind::Verb,
                lemma: Some("いう".to_string()),
            }],
            &RuleStore::new(),
        )
        .unwrap();
        assert_eq!(result.all[0].strokes, "nt-t/I-SKntk/-tk");
        assert!(
            result.all.iter().any(|c| c.strokes == "nt-t/I-SKntk/-tk"),
            "{:?}",
            result.all
        );
        assert!(
            result
                .basic_and_particle
                .iter()
                .any(|c| c.strokes == "nt-t/Itk-TIA/-tk"),
            "{:?}",
            result.basic_and_particle
        );
    }
    #[test]
    fn inherited_vowel_and_runtime_override_are_verified() {
        let inherited = lookup("きしし", &[], &RuleStore::new()).unwrap();
        assert!(
            inherited
                .basic_and_particle
                .iter()
                .any(|c| c.strokes == "KI-SI/S-"),
            "{:?}",
            inherited.basic_and_particle
        );
        let mut rules = RuleStore::new();
        rules
            .set(RuleKind::User, "KA-", "ねこ", "", crate::Context::Unknown)
            .unwrap();
        let edited = lookup("ねこ", &[], &rules).unwrap();
        assert!(edited.all.iter().any(|c| c.strokes == "KA-"));
    }
    #[test]
    fn compound_word_and_particle_have_separate_spans() {
        let parts = output_segments(
            "Knt-Tt",
            Kind::General,
            "こととは",
            State::default(),
            &RuleStore::new(),
            0,
        );
        assert_eq!(
            parts,
            std::vec![
                Segment {
                    start: 0,
                    end: 2,
                    kind: Kind::General,
                    lemma: None
                },
                Segment {
                    start: 2,
                    end: 4,
                    kind: Kind::Particle,
                    lemma: None
                },
            ]
        );
    }
    #[test]
    fn hash_repetition_can_be_shorter_than_basic_route() {
        let result = lookup("かたかた", &[], &RuleStore::new()).unwrap();
        assert!(
            result.all.iter().any(|c| c.strokes == "#KA-TA"),
            "{:?}",
            result.all
        );
    }
    #[test]
    fn two_new_composite_dictionary_parts_are_searchable() {
        let mut rules = RuleStore::new();
        rules
            .set(
                RuleKind::GeneralLeft,
                "KA",
                "こ",
                "",
                crate::Context::Unknown,
            )
            .unwrap();
        rules
            .set(
                RuleKind::GeneralRight,
                "K",
                "ね",
                "",
                crate::Context::Unknown,
            )
            .unwrap();
        let result = lookup("こね", &[], &rules).unwrap();
        assert!(
            result.all.iter().any(|c| c.strokes == "KA-K*"),
            "{:?}",
            result.all
        );
    }
}
