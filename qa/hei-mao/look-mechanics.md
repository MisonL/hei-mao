# hei-mao look mechanics

## Stable construction

- The shoes, lower blue overalls, and hip remain the grounded anchor on a shared baseline.
- The rounded dark-brown head and pink snout lead the gaze. The eyelids, ears, and small facial lines follow the head turn without changing the character identity.
- The white striped shirt, blue overalls, red gloves, and shoe proportions remain attached to the torso. The standard-row props stay attached and do not float or cross to the opposite side.

## Cardinal pose families

- `000` up: the snout and face pitch toward the top edge, the lower face becomes less prominent, and the ears follow upward while the feet and lower body stay fixed.
- `090` screen-right: the head and snout yaw toward the viewer's right; the snout tip moves to the right side of the head center and the right cheek becomes more visible.
- `180` down: the snout and eyelids pitch toward the bottom edge, the chin lowers slightly, and the torso and overalls remain grounded.
- `270` screen-left: the head and snout yaw toward the viewer's left; the snout tip moves to the left side of the head center and the left cheek becomes more visible.

## Intermediate motion

Each 22.5-degree step advances head yaw or pitch, eyelid/ear follow-through, and restrained upper-body movement by a similar visual amount. The lower-body anchor, apparent scale, costume, and shoe baseline stay stable across both rows. The 157.5 -> 180 and 337.5 -> 000 boundaries are one-step transitions with no snap or whole-sprite rotation.

The original face construction is preserved; do not add replacement eyes, detached pupils, text, shadows, glows, or other effects. Directions use viewer/screen coordinates and form one clockwise loop.
