"""
Utility functions for manipulating discord.py related objects etc.
"""


def extract_clean_message(ctx):
    """
    Returns the message cleaned from the command used to call the bot without leading or trailing whitespaces
    """
    message_content = ctx.message.content
    return message_content.replace(ctx.invoked_with, "").replace(ctx.prefix, "").strip()
