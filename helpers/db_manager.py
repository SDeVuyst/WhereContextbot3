import os
import psycopg2

""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""
async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, created_at FROM blacklist"
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM blacklist WHERE user_id=%s", (str(user_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, geven we geen toegang tot de bot
        except:
            return True
        

async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """

    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("INSERT INTO blacklist(user_id) VALUES (%s)", (str(user_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM blacklist")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM blacklist WHERE user_id=%s", (str(user_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM blacklist")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1


async def get_ooc_messages(limit: int) -> list:
    """
    This function will return a list of random ooc messages.

    :param limit: The amount of randomy selected messages
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT message_id, added_at, added_by, times_played FROM context_message ORDER BY random() LIMIT %s", (limit,)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def get_ooc_message(id) -> list:
    """
    This function will return a list of random ooc messages.

    :param limit: The amount of randomy selected messages
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT message_id, added_at, added_by, times_played FROM context_message WHERE message_id=%s", (str(id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def is_in_ooc(message_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM context_message WHERE message_id=%s", (str(message_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat bericht al in db zit
        except:
            return True
        

async def increment_times_played(message_id):
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "UPDATE context_message SET times_played = times_played + 1 WHERE message_id=%s", (str(message_id),)
                )
                con.commit()
                return True

        except:
            return False


async def add_message_to_ooc(message_id:int, added_by:int) -> int:
    """
    This function will add a OOC message based on its ID in the blacklist.

    :param message_id: The ID of the message that should be added.
    :param added_by: The ID of the user who submitted the message.
    :param about: The ID of the user whom the message is about.

    """

    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO context_message(message_id, added_by) VALUES (%s, %s)",
                    (str(message_id), str(added_by),)
                )
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM context_message")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
    except Exception as err:
        return -1


async def remove_message_from_ooc(message_id: int) -> int:
    """
    This function will remove a message based on its ID from the ooc game.

    :param message_id: The ID of the message that should be removed from the game.
    """
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute("DELETE FROM context_message WHERE message_id=%s", (str(message_id),))
                con.commit()
                cursor.execute("SELECT COUNT(*) FROM context_message")
                result = cursor.fetchone()
                return result[0] if result is not None else 0
            
    except:
        return -1
    

async def increment_or_add_nword(user_id: int):

    alreadyExists = await is_in_ncounter(user_id)

    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE nword_counter SET count = count + 1 WHERE user_id=%s", (str(user_id),)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO nword_counter(user_id, count) VALUES (%s, %s)",
                        (str(user_id), 1,)
                    )

                cursor.commit()
                return True
                
        except:
            return False
    

async def is_in_ncounter(user_id: int) -> bool:
    """
    This function will check if a user exists in counter.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user exists, False if not.
    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM nword_counter WHERE user_id=%s", (str(user_id),)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat bericht al in db zit
        except:
            return True
        

async def get_nword_count(user_id) -> list:
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT count FROM nword_counter WHERE user_id=%s", (str(user_id),)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]


async def get_nword_leaderboard() -> list:
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, count FROM nword_counter ORDER BY count DESC LIMIT 10"
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    

async def set_nword_count(user_id, amount):
    alreadyExists = await is_in_ncounter(user_id)

    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE nword_counter SET count = %s WHERE user_id=%s", ((amount), str(user_id),)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO nword_counter(user_id, count) VALUES (%s, %s)",
                        (str(user_id), amount,)
                    )
                    
                con.commit()
                return True

        except:
            return False
        


async def is_in_command_count(user_id: int, command_name: str) -> bool:
    """
    This function will check if a user already played a command.

    """
        
    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM command_stats WHERE user_id=%s AND command=%s", (str(user_id), command_name,)
                )
                result = cursor.fetchall()
                return len(result) > 0
        # Als er iets misgaat, zeggen we dat command al bestaat
        except:
            return True
        

async def increment_or_add_command_count(user_id: int, command_name: str, amount: int):

    alreadyExists = await is_in_command_count(user_id, command_name)

    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE command_stats SET count = count + %s WHERE user_id=%s AND command=%s",
                        (amount, str(user_id), command_name)
                    )   
                else:
                    cursor.execute(
                        "INSERT INTO command_stats(command, user_id, count) VALUES (%s, %s, %s)",
                        (command_name, str(user_id), amount,)
                    )

                cursor.commit()
                return True
                
        except:
            return False
        

async def set_command_count(command_name, user_id, amount):
    alreadyExists = await is_in_command_count(user_id, command_name)

    with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
        
        try:
            with con.cursor() as cursor:
                if alreadyExists:
                    cursor.execute(
                        "UPDATE command_stats SET count = %s WHERE user_id=%s  AND command=%s", 
                        ((amount), str(user_id), command_name,)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO command_stats(command, user_id, count) VALUES (%s, %s, %s)",
                        (command_name, str(user_id), amount,)
                    )
                    
                con.commit()
                return True

        except:
            return False
        

async def get_command_count(user_id, command_name) -> list:
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT count FROM command_stats WHERE user_id=%s AND command=%s", 
                    (str(user_id), command_name,)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    


async def get_leaderboard(command: str) -> list:
    try:
        with psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require') as con:
            
            with con.cursor() as cursor:
                cursor.execute(
                    "SELECT  user_id, count FROM command_stats WHERE command=%s ORDER BY count DESC LIMIT 10", 
                    (command,)
                )
                return cursor.fetchall()
            
    except Exception as err:
        return [-1, err]
    