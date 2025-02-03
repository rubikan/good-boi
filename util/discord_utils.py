"""
Utility functions for manipulating discord.py related objects etc.
"""


def extract_clean_message(ctx):
    """
    Returns the message cleaned from the command used to call the bot without leading or trailing whitespaces
    """
    message_content = ctx.message.content
    message_content = message_content.replace(ctx.invoked_with, "").replace(
        ctx.prefix, ""
    )
    for parent in ctx.invoked_parents:
        message_content = message_content.replace(parent, "")
    return message_content.strip()
