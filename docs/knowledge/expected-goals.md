# Expected Goals (xG)

## Definition

Expected goals (xG) estimates the probability that a shot will result in a goal. Each shot receives a value between 0 and 1.

For example, a shot worth 0.30 xG has an estimated 30% chance of becoming a goal according to the model. It does not guarantee the outcome of that particular attempt.

Models estimate these probabilities using historical data and shot characteristics such as location, angle and body part. Some models also use goalkeeper and defender positions. Different providers can assign different xG values to the same chance.

## Calculation in this project

This project uses StatsBomb's supplied xG values rather than training its own model.

The `shot_statsbomb_xg` field contains the xG value for an individual shot. Team match summaries sum this field for events whose `type` is `Shot`, grouping by match and team.

For example, shots worth 0.50 and 0.20 xG produce a total of 0.70 xG, regardless of whether either shot resulted in a goal.

Analytics preserve the available numeric precision. Match reports display xG rounded to two decimal places.

## Own goals

Own-goal events contribute to the project's goal count but do not add xG. The goal calculation includes successful shots and `Own Goal For` events.

A team could therefore win 1–0 through an own goal while recording no shots and zero xG.

## Interpretation and limitations

- xG describes the chances represented by recorded shots. It does not capture every dangerous attack, including those without a shot.
- A team's total xG is an expected goal count, not its probability of winning.
- Higher xG alone does not establish that a team dominated or deserved to win.
- Goals and xG can differ substantially in an individual match.
- Values from different providers or model versions are not necessarily directly comparable.
- Missing xG on a shot is missing information, not evidence that the shot had zero scoring probability. Checking that the column exists does not establish that every shot has a value.

## Sources

- [StatsBomb: Upgrading Expected Goals](https://www.hudl.com/blog/upgrading-expected-goals)
- [StatsBomb Open Data specification](https://github.com/statsbomb/open-data/tree/master/doc)

The calculation and reporting rules above describe this project's implementation.