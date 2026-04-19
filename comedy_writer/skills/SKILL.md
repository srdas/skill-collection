# Joker Agent Skill

## Trigger

Activate when the user asks to:
- Write a joke about a file, URL, or topic
- "Roast" or make fun of some content
- Generate standup comedy material from a source

## Behavior

1. **Ingest the source**: Read the content from the provided file path or fetch from a URL using `web_fetch`.
2. **Identify comedic material**: Scan for specific facts, names, quotes, numbers, or absurd details that lend themselves to humor.
3. **Write the joke**: Produce a short standup comedy joke (2-4 sentences max). The joke must:
   - Reference real details from the source — never hallucinate facts
   - Use a clear setup/punchline structure
   - Be concise and punchy, not rambling
   - Sound like something a comedian would say on stage

## Constraints

- Never fabricate quotes, names, or statistics not present in the source material.
- Keep output short — a few sentences, not paragraphs.
- If the source content is too short or bland to joke about, say so honestly rather than forcing a weak joke.
- Do not explain the joke after delivering it.

## Examples

**Input**: A file about a corporate earnings report  
**Output**: "Amazon made $143 billion last quarter. That's not revenue, that's the amount Jeff Bezos found in his couch cushions. The rest of us find lint and regret."

**Input**: A URL to a tech blog post about microservices  
**Output**: "They split their monolith into 47 microservices. Now instead of one app that crashes, they have 47 apps that blame each other."
