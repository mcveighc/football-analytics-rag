# Understanding Match Summaries

## Purpose

A match summary combines team-level event statistics with match metadata. Each row represents one team in one match.

A generated match report presents the home team first and the away team second, regardless of which team has more goals, shots or xG.

## Fields

- `match_id`: identifies the match.
- `match_date`: the date recorded in match metadata.
- `team`: the team whose statistics appear in the row.
- `opponent`: the other team, determined from match metadata.
- `home_or_away`: whether the team is listed as home or away.
- `shots`: the number of events whose `type` is `Shot`.
- `goals`: successful shot events plus `Own Goal For` events.
- `total_xg`: the sum of `shot_statsbomb_xg` for shot events.

## Counting shots

Every event labelled `Shot` contributes one attempt. The count does not depend on whether the shot scored or whether its outcome is present.

A null `shot_outcome` on a pass or another non-shot event is expected: the field does not apply to that event.

A null outcome on a shot represents missing information about the attempt's result. It does not erase the recorded attempt.

## Teams with no shots

The query retains non-shot events before grouping, allowing a team with recorded events but no shots to appear with zero shots and zero xG.

A team with no event rows at all is not created automatically from match metadata. Missing event data should not be interpreted as a verified zero-shot performance.

## Joining match metadata

Event statistics are associated with metadata using `match_id`. The metadata supplies the date and identifies the home and away teams.

The current query assumes one metadata row per match ID. Duplicate metadata rows can multiply joined events and inflate totals.

The query uses an inner join, so events without matching metadata are excluded from the result.

## Multiple matches

Statistics are grouped by match and team. The same team appearing in two matches therefore receives separate summary rows.

Generated reports describe a single selected match.

## Reading the report

In a line such as:

    Shots: 11-22

the home team recorded 11 shots and the away team recorded 22.

Expected goals are displayed to two decimal places. The underlying analytics retain the available precision, so a displayed 0.00 can represent a small positive value rounded for presentation.

## Choosing analytics or document retrieval

Use structured analytics for exact calculations, rankings and comparisons across matches.

Use knowledge notes to explain metric definitions and calculation rules. Use generated reports to retrieve descriptive context about specific matches.

A text search returns matching documents; it does not calculate statistics across the underlying dataset.

## Related notes

- [Expected Goals](expected-goals.md)
- [Goals and Own Goals](goals.md)

This document describes the project's current query and report behaviour.