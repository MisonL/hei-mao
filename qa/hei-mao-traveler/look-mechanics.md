# Traveler look mechanics

## Natural motion

Traveler is a soft, grounded chibi pig with a flexible neck, expressive eyes, attached leafy vegetables, a rigid green backpack, and a small orange-red fortune pouch. The lower feet and hip stay registered as the anchor. The head and snout lead the gaze, the pupils and eyelids follow the head turn, and the upper torso bends slightly. The backpack stays attached to the torso and lags only by a small amount; the fortune pouch follows the hip and remains on the same body side. The leafy vegetables sway with the hand and torso but never detach.

## Cardinal pose families

- `000 up`: feet and hip stay grounded; chin and snout lift toward the top of the image, pupils rise, eyelids open upward, and the top of the head becomes more visible.
- `090 right`: screen-right face turn; snout and pupils move to the right of head center, the left cheek and left side of the backpack become more visible, and the right-side facial contour leads.
- `180 down`: chin and snout angle toward the bottom of the image, pupils lower, eyelids narrow downward, and the forehead/top of head remains visible while the muzzle points down.
- `270 left`: screen-left face turn; snout and pupils move to the left of head center, the right cheek and right side of the backpack become more visible, and the left-side facial contour leads.

## Motion budget

Each 22.5-degree step changes the head turn, snout, pupils, eyelids, and upper torso by a similar visual amount. Feet, hip, backpack attachment, and pouch registration stay stable. Diagonals interpolate the adjacent cardinal face and torso families; no whole-sprite rotation, skew, or independent cell restyling is allowed.
