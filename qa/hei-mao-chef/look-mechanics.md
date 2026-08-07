# hei-mao-chef look mechanics

## Character construction

The chef is a compact humanoid pig mascot with a rounded dark-brown head, a pink snout, closed curved eyes, two ears, a white chef toque, white sleeves, a red apron, dark trousers, and brown shoes. The feet and shoe soles are the grounded anchor. The apron lower hem and torso remain stable so a gaze change does not look like a body translation.

## Natural look motion

- The head and snout lead the gaze. The face plane turns or pitches toward the target while preserving the original snout, eye-arc, ear, and head proportions.
- The closed eye arcs are redrawn as part of the face turn. Do not slide pupils, add eye whites, or paint replacement googly eyes; this character has no visible pupils.
- Ears follow the head with a small, continuous lag. The chef toque follows the head and may compress or reveal a little more side rim, but must not float or change size independently.
- The upper torso and shoulder line follow subtly. The red apron, straps, pocket, buttons, sleeves, gloves, trousers, and shoes remain attached to the body; the apron hem and shoe baseline stay registered.
- No cooking utensil, food, text, symbol, motion mark, shadow, glow, or detached effect is introduced in look cells. The hands remain empty and close to the existing silhouette.

## Cardinal pose families

- `000` up: the snout and face plane pitch upward; the lower head edge and chin become less visible, the toque underside becomes slightly more visible, and the ears follow upward. The shoes and apron hem stay fixed.
- `090` screen-right: the head and snout yaw toward the viewer's right. The snout shifts to the right side of the head center, the right cheek/ear reads more prominently, and the opposite cheek becomes partly occluded. The torso follows only slightly.
- `180` down: the head and face plane pitch downward; the toque top and forehead become less prominent, the snout drops toward the lower face, and the apron front remains anchored below.
- `270` screen-left: the head and snout yaw toward the viewer's left. The snout shifts to the left side of the head center, the left cheek/ear reads more prominently, and the opposite cheek becomes partly occluded. This must visibly oppose `090` in screen coordinates.

## Motion budget and interpolation

Each 22.5 degree step advances the head yaw or pitch by a similar visual amount. The stable lower-body anchor is shared across all directions. Intermediate poses blend yaw and pitch between neighboring cardinal families, with ear and toque follow-through kept smaller than the head movement. The row boundary `157.5 -> 180` and loop boundary `337.5 -> 000` must remain one-step transitions without a scale, baseline, or identity jump.

## Direction acceptance

All directions use viewer/screen coordinates. Cardinals must be unmistakable at normal pet size. Diagonals must preserve both intended axes through head, snout, eye-arc, ear, and toque evidence. A pose that remains front-facing, rotates the whole sprite, changes the apron or shoe registration, or introduces a new facial design is rejected and requires regeneration of the complete coherent row.
