# Goals and Own Goals

## Definition

A team's score includes goals scored through its own shots and own goals awarded to it when the opposition scores into their own net.

In StatsBomb event data, own goals are separate event types rather than a dedicated shot outcome.

## Calculation in this project

The team match summary counts an event as a goal when either:

- `type` is `Shot` and `shot_outcome` is `Goal`.
- `type` is `Own Goal For`.

Results are grouped by `match_id` and `team`.

## Own goals

`Own Goal For` identifies an own goal awarded to the event's team.
`Own Goal Against` identifies an own goal conceded by the event's team.

The calculation uses `Own Goal For` when adding to a team's score.
It does not also count `Own Goal Against` as a goal for that team.

Own-goal events do not increase the project's shot count or xG total.

For example, a team with one successful shot and one own goal awarded to it has two goals. The own goal adds no shot and no xG.

## Event-derived score

Match reports label the score as "from event data" because it is calculated from events rather than copied from match metadata.

The match metadata's `home_score` and `away_score` provide a separate reference for checking the calculation.

A mismatch should be investigated rather than silently overwritten.
Possible causes include incomplete event data or incorrect aggregation.

## Scope and limitations

The current calculation counts qualifying events across all periods present in the input. It does not implement a separate penalty-shootout policy. Before applying it to matches with shootouts, define how shootout events should be excluded from the match score and reported separately.

A missing `shot_outcome` on a recorded shot is incomplete information. The current goal condition will not count that shot as a goal, but this does not establish that it was a non-goal.

## Sources

- [StatsBomb Open Data specification](https://github.com/statsbomb/open-data/tree/master/doc)

The aggregation rules above describe this project's implementation.