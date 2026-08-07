# hei-mao-quality look mechanics

## Stable construction

- The feet, lower legs, hips, and lower torso stay anchored to the cell baseline.
- The square-rounded head and short black forelock lead the look. The eyes, eyelids, snout, and ear angles follow the head turn; the face must remain the same pig identity.
- The white quality-control uniform stays rigid around the torso. The blue gloves remain attached to the arms.
- The circular magnifying glass is a rigid chest prop attached by its handle and cord. It follows the upper torso with a small lag and may become partly occluded by the head or arm, but it never detaches.
- The leafy greens are a hand-held prop on the pet's screen-right side in the front view. They follow the hand and lag the upper body slightly while staying attached, readable, and outside the face.

## Cardinal pose families

- `000` up: eyes and snout angle upward, upper head lifts slightly, ears follow upward, and the lower body stays fixed.
- `090` screen-right: head and face turn right; the nose tip and pupils move to the right side of the head center, with the screen-right cheek more visible. The magnifying glass and greens remain attached and shift only with the upper torso.
- `180` down: eyelids and snout angle downward, chin lowers slightly, and the upper torso compresses subtly without changing the anchored feet.
- `270` screen-left: head and face turn left; the nose tip and pupils move to the left side of the head center, with the screen-left cheek more visible. The props remain attached and oppose the right-facing family.

## Intermediate motion budget

Each 22.5-degree step moves the eyes, eyelids, snout, ear angles, head, and constrained props by a similar visual amount. The torso and baseline do not jump. Diagonals interpolate between the adjacent cardinal families, and the direction order is clockwise in viewer coordinates.

Do not rotate the whole sprite, replace the eye construction, add new eyes, add text or symbols, or introduce scenery, shadows, glows, or detached effects.
