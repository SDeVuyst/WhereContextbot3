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
    async with psycopg2.connect(
        database=os.environ.get("Database"),
        user=os.environ.get("User"),
        password=os.environ.get("Password"),
        host=os.environ.get("Host"),
        port= os.environ.get("Port")

    ) as con:
        
        async with (con.cursor().execute(
            "SELECT user_id, strftime('%s', created_at) FROM blacklist"
        )) as cursor:
            return await cursor.fetchall()
    


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
        
    async with psycopg2.connect(
        database=os.environ.get("Database"),
        user=os.environ.get("User"),
        password=os.environ.get("Password"),
        host=os.environ.get("Host"),
        port= os.environ.get("Port")
        
    ) as con:
        
        async with (con.cursor().execute(
            "SELECT * FROM blacklist WHERE user_id=?", (user_id,)
        )) as cursor:
            result = await cursor.fetchall()
            return result is not None
        


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    # async with aiosqlite.connect(DATABASE_PATH) as db:
    #     await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
    #     await db.commit()
    #     rows = await db.execute("SELECT COUNT(*) FROM blacklist")
    #     async with rows as cursor:
    #         result = await cursor.fetchone()
    #         return result[0] if result is not None else 0
        

    async with psycopg2.connect(
        database=os.environ.get("Database"),
        user=os.environ.get("User"),
        password=os.environ.get("Password"),
        host=os.environ.get("Host"),
        port= os.environ.get("Port")
        
    ) as con:
        
        async with (con.cursor()) as cursor:
            await cursor.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
            await cursor.commit()
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    # async with aiosqlite.connect(DATABASE_PATH) as db:
    #     await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
    #     await db.commit()
    #     rows = await db.execute("SELECT COUNT(*) FROM blacklist")
    #     async with rows as cursor:
    #         result = await cursor.fetchone()
    #         return result[0] if result is not None else 0
        
    async with psycopg2.connect(
        database=os.environ.get("Database"),
        user=os.environ.get("User"),
        password=os.environ.get("Password"),
        host=os.environ.get("Host"),
        port= os.environ.get("Port")
        
    ) as con:
        
        async with (con.cursor()) as cursor:
            await cursor.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
            await cursor.commit()
            result = await cursor.fetchone()
            return result[0] if result is not None else 0
