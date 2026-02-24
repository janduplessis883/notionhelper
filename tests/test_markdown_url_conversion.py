from notionhelper import NotionHelper


def test_extract_rich_text_uses_text_link_url():
    helper = NotionHelper("test-token")
    rich_text = [
        {
            "type": "text",
            "text": {"content": "OpenAI", "link": {"url": "https://openai.com"}},
            "href": None,
            "annotations": {},
        }
    ]

    markdown = helper._extract_rich_text(rich_text)

    assert markdown == "[OpenAI](https://openai.com)"


def test_extract_rich_text_falls_back_to_plain_text_for_mentions():
    helper = NotionHelper("test-token")
    rich_text = [
        {
            "type": "mention",
            "plain_text": "https://example.com/docs",
            "href": "https://example.com/docs",
            "annotations": {},
        }
    ]

    markdown = helper._extract_rich_text(rich_text)

    assert markdown == "[https://example.com/docs](https://example.com/docs)"


def test_blocks_to_markdown_renders_url_blocks():
    helper = NotionHelper("test-token")
    blocks = [
        {"type": "bookmark", "bookmark": {"url": "https://example.com/bookmark"}},
        {"type": "embed", "embed": {"url": "https://example.com/embed"}},
        {"type": "link_preview", "link_preview": {"url": "https://example.com/preview"}},
    ]

    markdown = helper._blocks_to_markdown(blocks)

    assert "[https://example.com/bookmark](https://example.com/bookmark)" in markdown
    assert "[https://example.com/embed](https://example.com/embed)" in markdown
    assert "[https://example.com/preview](https://example.com/preview)" in markdown
