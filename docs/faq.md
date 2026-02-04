# FAQ

## Does Naturally Linux run commands automatically?

No. It always shows the generated command and asks for confirmation unless you pass `--yes`.

## Why do I need a Groq API key?

The command generator uses Groq’s LLM API. Each user should provide their own API key.

## Can I use a different model provider?

Yes. Replace the Groq client in `generator.py` with your provider of choice.

## Is this safe for production servers?

Review every command. The current safety filter is basic and does not replace human judgment.
