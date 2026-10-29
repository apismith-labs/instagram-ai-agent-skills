# Use Instagram Transcript Extractor in ChatGPT

This guide describes the documented setup flow. It is not evidence that the full flow has passed project testing. Historical ChatGPT task reports used an upload whose version is unknown; a transcript task using the v0.1.0 Release ZIP together with Apify authorization remains unverified. See the [test status](../test-status.md).

## Before you start

You need your own [Apify account](https://console.apify.com/). Actor runs use the allowance and billing terms of that account; the [Apify Console](https://console.apify.com/) shows current Runs and billing details.

ChatGPT Skills availability depends on account, workspace, and product availability. OpenAI's [Skills in ChatGPT guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) currently documents Skills for eligible Business, Enterprise, Healthcare, and Edu users, but availability may vary. The project owner reported seeing the Skills page on a Plus account; that does not confirm Plus availability for everyone.

## 1. Connect and authorize Apify

Apify connection and Skill installation are separate steps. The Apify connection gives ChatGPT access to external Apify tools; the Skill supplies the transcript workflow.

1. In ChatGPT, open **Plugins → + → Add custom MCP server**.
2. Enter a name such as `Apify` and set the Server URL to `https://mcp.apify.com`.
3. Choose **OAuth** in the authentication options and complete the Apify authorization.
4. Review the risk notice and continue. Choose **Create as a plugin**.
5. Review the discovered tools and metadata, then install the generated plugin.

These steps follow the current [OpenAI custom MCP server guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt). The interface and account/workspace permissions can change. OpenAI's current documentation says custom MCP server creation is available on ChatGPT web for Business and Enterprise/Edu, with workspace roles controlling who may create or publish connections. Business workspace creation is limited to admins and owners; Enterprise/Edu admins may grant selected members permission to create connections, while only admins or owners publish workspace apps. Personal plugin installation is not the same as publishing to a workspace. Plus custom MCP creation rights are not confirmed by this project. If the option is missing, check your plan and workspace permissions and ask your workspace administrator if needed.

## 2. Upload the Skill

Download `instagram-transcript-extractor.zip` from the [v0.1.0 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip), or open the [Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.1.0) and choose that named file under **Assets**. Do not download GitHub's automatically generated **Source code (zip)**. Optional SHA-256 check:

```text
cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331
```

Keep the downloaded ZIP intact; do not unzip it before upload. In ChatGPT, open **Plugins → Skills → Create → Upload from your computer**, then select `instagram-transcript-extractor.zip`. Wait for the upload scan. The Skill may become **Available**, show **Needs Review**, or show **Blocked**:

- **Available:** continue to a new conversation.
- **Needs Review:** read the displayed prompt and follow the review step before using it.
- **Blocked:** the Skill cannot be used in that state. The scan status alone does not show that the ZIP is damaged. Avoid repeatedly uploading the same ZIP. Note the release version and scan message, then [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) for help. Do not include credentials or personal sensitive information.

The project owner reported that the v0.1.0 ZIP initially appeared in the Skills list with its Instagram brand icon. After reloading the editor, the owner reported that the downloaded editor package had rewritten both icon references to a generic `assets/icon.svg`. This is an editor round-trip report, not a guarantee about later imports or edits; details are in the [test status](../test-status.md).

## 3. Use it in a new conversation

Start a new conversation. In the message box, type **@** and select the installed Apify plugin. The connection may apply per message, so select it again in a later message if that message needs new Apify data.

For example, replace the sample URL with a real public Instagram Reel or supported video post link:

```text
Use Instagram Transcript Extractor to get the transcript of this public Instagram Reel:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

The report of earlier ChatGPT transcript tasks came from a separately uploaded version that has not been identified as the v0.1.0 ZIP. Those reports do not verify this complete Release ZIP → Apify authorization → transcript journey.
