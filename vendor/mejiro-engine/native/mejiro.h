#ifndef MEJIRO_ENGINE_H
#define MEJIRO_ENGINE_H
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#ifdef __cplusplus
extern "C" {
#endif
/* ABI 1. All offsets/lengths are UTF-8 bytes, never Backspace counts.
 * State: vowel low nibble indexes A,I,U,IA,AU,YA,YU,YAU,Y,YI,YIA,YIU,YIAU,IU,IAU.
 * Its high nibble stores input mode: both=0, left=1, right=2.
 * Context: unknown, nominalizable, incomplete, attributive_na,
 * question_predicate, noun, place, indefinite_noun, question_particle (0..8).
 * Mode: kana=0, romaji=1, JIS=2. pending_sokuon is 0 or 1.
 * Macro indices: n,t,k,nt,nk,tk,ntk (0..6). */
typedef struct { uint8_t vowel, context, mode, pending_sokuon; } mejiro_state;
typedef enum {
    MEJIRO_KEY_NONE, MEJIRO_RETURN, MEJIRO_SPACE, MEJIRO_TAB, MEJIRO_BACKSPACE,
    MEJIRO_DELETE, MEJIRO_LEFT, MEJIRO_DOWN, MEJIRO_RIGHT, MEJIRO_UP,
    MEJIRO_HOME, MEJIRO_END, MEJIRO_SHIFT_LEFT, MEJIRO_SHIFT_DOWN,
    MEJIRO_SHIFT_RIGHT, MEJIRO_SHIFT_UP, MEJIRO_SHIFT_HOME, MEJIRO_SHIFT_END,
    MEJIRO_SHIFT_RETURN, MEJIRO_CTRL_RETURN, MEJIRO_F13, MEJIRO_F14,
    MEJIRO_SHIFT_0, MEJIRO_SELECT_ALTERNATE_SYSTEM, /* optional host-selected system */
    MEJIRO_IME_ON, MEJIRO_IME_OFF
} mejiro_key;
typedef struct { uint16_t byte_offset; uint8_t key, reserved; } mejiro_operation;
/* Additive host-recording API; existing translation/event ABI stays unchanged.
 * HID pages: keyboard=7, consumer=12, system=1. kind: mods=0, down=1, up=2.
 * Standard HID modifier bits. All reserved fields must be zero. */
typedef struct { uint16_t usage; uint8_t page, mods, kind, reserved; } mejiro_hid_event;
typedef struct { uint16_t byte_offset; uint8_t operation_index, reserved; mejiro_hid_event event; } mejiro_recorded_event;
#define MEJIRO_EXTERNAL_CAPACITY 128
int32_t mejiro_core_session_record_external(uint8_t *, const mejiro_hid_event *, size_t);
int32_t mejiro_core_session_replayed_external(const uint8_t *, mejiro_recorded_event *, size_t);
int32_t mejiro_core_session_abort_recordings(uint8_t *);
typedef struct {
    mejiro_state next;
    uint8_t text[512];
    uint16_t text_len;
    mejiro_operation operations[8];
    uint8_t operation_count, output_context, request, argument;
    uint8_t dynamic_particle, reserved;
} mejiro_translation;
/* Firmware core. Text is length-delimited, not NUL-terminated. Requests:
 * output=0, undo=1, repeat=2, toggle_typing=3, toggle_record=4, stop=5, replay=6.
 * Returns 0 on success, -1 invalid input, -2 capacity. */
int32_t mejiro_core_translate(const uint8_t *, size_t, const mejiro_state *,
                              uint8_t include_commands, mejiro_translation *);
/* Opaque runtime storage is caller-owned, must have the reported size and
 * alignment, and must be initialized before use. No allocator is required.
 * Context/state/undo/repeat/recording are shared with Rust Session<20>.
 * An undo with no history returns kind=1 and erase_units=2. */
typedef struct {
    mejiro_translation translation;
    uint32_t erase_units;
    uint64_t ticket;
    uint8_t kind, has_ticket, reserved[6];
} mejiro_event;
size_t mejiro_core_session_size(void);
size_t mejiro_core_session_align(void);
int32_t mejiro_core_session_init(uint8_t *storage, size_t capacity);
int32_t mejiro_core_session_process(uint8_t *session, const uint8_t *stroke,
                                    size_t len, mejiro_event *output);
int32_t mejiro_core_session_ack(uint8_t *session, uint64_t ticket, uint32_t units);
int32_t mejiro_core_session_reset(uint8_t *session);
int32_t mejiro_core_session_set_typing_mode(uint8_t *session, uint8_t mode);
/* Runtime dictionary overlay. Kinds: user=0, general=1,
 * general-left=2, general-right=3, verb=4. General context 0 infers
 * grammar from the word; 1..8 use an explicit context.
 * Each edit clears linguistic state/history, retaining macros and mode.
 * Host owns persistence: enumerate entries and restore them after init.
 * set/hide/clear return 0, -1 invalid, -2 full/too long.
 * get returns 0 or -3 when index is beyond the overlay length. */
#define MEJIRO_RULE_CAPACITY 24
#define MEJIRO_RULE_KEY_CAPACITY 32
#define MEJIRO_RULE_VALUE_CAPACITY 96
#define MEJIRO_RULE_ROW_CAPACITY 8
typedef struct {
    uint8_t kind, context, hidden, key_len;
    uint8_t value_len, row_len, reserved[2];
    uint8_t key[MEJIRO_RULE_KEY_CAPACITY];
    uint8_t value[MEJIRO_RULE_VALUE_CAPACITY];
    uint8_t row[MEJIRO_RULE_ROW_CAPACITY];
} mejiro_rule;
int32_t mejiro_core_session_rule_set(uint8_t *session, const mejiro_rule *rule);
int32_t mejiro_core_session_rule_hide(uint8_t *session, uint8_t kind,
                                     const uint8_t *key, size_t key_len);
int32_t mejiro_core_session_rule_clear(uint8_t *session, uint8_t kind,
                                      const uint8_t *key, size_t key_len);
int32_t mejiro_core_session_rule_count(const uint8_t *session);
int32_t mejiro_core_session_rule_get(const uint8_t *session, size_t index,
                                    mejiro_rule *output);
int32_t mejiro_core_session_rule_clear_all(uint8_t *session);
/* Desktop bridge: Plover body is NUL terminated. Returns -3 for controls.
 * Rust Session owns runtime controls; this function is a pure preview. */
uint32_t mejiro_abi_version(void);
/* Plover confirmed-history preview; supports all control requests (0..6).
 * No argument is modified on failure. */
int32_t mejiro_plover_preview(const uint8_t *, size_t, const mejiro_state *,
                              uint8_t *, size_t, mejiro_state *,
                              uint8_t *request, uint8_t *argument);
int32_t mejiro_plover_override(const uint8_t *, size_t, const mejiro_state *,
                               uint8_t *, size_t, mejiro_state *);
int32_t mejiro_translate(const uint8_t *, size_t, const mejiro_state *, bool,
                         uint8_t *, size_t, mejiro_state *, uint8_t *output_context);
#ifdef __cplusplus
}
#endif
#endif
