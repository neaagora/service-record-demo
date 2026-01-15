# service-record-demo

This repository is a **proof of concept** that demonstrates how observed AI agent behavior can be recorded into a **service record artifact**.

The artifact is designed to be consumed later by external systems, such as agent directories or policy engines, without changing how those systems normally operate.

This repo does **not** rank agents.
It does **not** enforce policy.
It only records what happened.

## What this demo shows

-   An AI agent performs a task.

-   The task does not complete autonomously.

-   Human escalation is required.

-   That outcome is recorded as a structured **service record**.

-   The record is saved as a portable JSON artifact.

The artifact can then be used elsewhere to influence decisions, such as whether an agent should be recommended for autonomous use.

## What a service record is (in this demo)

A service record is a small JSON file that captures:

-   which agent was involved

-   what was observed during execution

-   whether escalation or intervention was required

-   basic metadata about the interaction

In this demo, the key signal is the descriptor:

```
needs_escalation

```

This indicates the agent could not safely complete the task on its own.



## What this repo intentionally does NOT do

-   It does not define a standard or schema.

-   It does not claim authority over trust or safety.

-   It does not decide how directories or platforms must react.

-   It does not modify agent rankings.

Those decisions are left to downstream systems.

## How this repo is used with other demos

This repository pairs with a separate directory demo:

-   `dir-trust-ranking-poc`

In that demo:

-   A directory ranks agents as usual.

-   A service record generated here is loaded.

-   A simple policy overlay reacts to the recorded behavior.

-   The directory recommendation changes, without changing base ranking logic.

This repo answers the question:

> "How do we record what actually happened?"

The directory demo answers:

> "What can a system do with that record?"

## Quickstart

1. Clone this repository
2. Run `python generate_service_record.py`
3. Check `artifacts/` for generated service records
4. See the companion `dir-trust-ranking-poc` demo for how these records are consumed
   
## Running the demo

This repository produces example service record artifacts under:

```
artifacts/

```

For example:

```
artifacts/service_record__agent-gamma.json

```

These files are meant to be consumed by other tools or demos.

Refer to the companion directory demo for how the artifact is used downstream.

## Scope and intent

This is a **minimal, illustrative demo**.

It exists to make one point clear:

> Real-world agent behavior can be recorded independently of the systems that later evaluate or act on it.

Nothing more is claimed.
