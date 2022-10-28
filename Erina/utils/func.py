from pyrogram.types import Message
from datetime import datetime, timedelta

async def extract_userid(message, text: str):
  """
  NOT TO BE USED OUTSIDE THIS FILE
  """

  def is_int(text: str):
    try:
      int(text)
    except ValueError:
      return False
    return True

  text = text.strip()

  if is_int(text):
    return int(text)

  entities = message.entities
  app = message._client
  if len(entities) < 1:
    return (await app.get_users(text)).id
  entity = entities[0]
  if entity.type == "mention":
    return (await app.get_users(text)).id
  if entity.type == "text_mention":
    return entity.user.id
  return None


async def extract_user_and_reason(message, sender_chat=False, texr=None):
  if texr:
    args = texr.strip().split()
  else:
    args = []
  text = texr
  user = None
  reason = None
  if message.reply_to_message:
    reply = message.reply_to_message
    # if reply to a message and no reason is given
    if not reply.from_user:
      if (
          reply.sender_chat
          and reply.sender_chat != message.chat.id
          and sender_chat
      ):
        id_ = reply.sender_chat.id
      else:
        return None, None
    else:
      id_ = reply.from_user.id

    if len(args) < 1:
      reason = None
    else:
      reason = text
    return id_, reason

  # if not reply to a message and no reason is given
  if len(args) == 1:
    user = args[0]
    return await extract_userid(message, user), None

  # if reason is given
  if len(args) > 1:
    user, reason = text.split(None, 1)
    return await extract_userid(message, user), reason

  return user, reason


async def time_converter(message: Message, time_value: str) -> int:
  unit = ["m", "h", "d"]  # m == minutes | h == hours | d == days
  check_unit = "".join(list(filter(time_value[-1].lower().endswith, unit)))
  currunt_time = datetime.now()
  time_digit = time_value[:-1]
  if not time_digit.isdigit():
    return await message.reply_text("Incorrect time specified")
  if check_unit == "m":
    temp_time = currunt_time + timedelta(minutes=int(time_digit))
  elif check_unit == "h":
    temp_time = currunt_time + timedelta(hours=int(time_digit))
  elif check_unit == "d":
    temp_time = currunt_time + timedelta(days=int(time_digit))
  else:
    return await message.reply_text("Incorrect time specified.")
  return int(datetime.timestamp(temp_time))
