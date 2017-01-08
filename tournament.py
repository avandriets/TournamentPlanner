#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    conn = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""DELETE FROM Matches;""")

        conn.commit()
    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()
        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()


def deletePlayers():
    """Remove all the player records from the database."""

    conn = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""DELETE FROM Players;""")
        conn.commit()

    except psycopg2.DatabaseError, e:
        if conn:
            conn.rollback()

        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""SELECT count(*) FROM Players;""")
        rows = cur.fetchall()

        for row in rows:
            return row[0]

    except psycopg2.DatabaseError, e:

        if conn:
            conn.rollback()

        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()

    return 0


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    conn = None

    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("""INSERT INTO Players (name) VALUES (%s);""", (name,))

        conn.commit()

    except psycopg2.DatabaseError, e:

        if conn:
            conn.rollback()

        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT Players.id, Players.name, COUNT(DISTINCT win.id )
                AS wins, COUNT(DISTINCT loss.id) + COUNT(DISTINCT win.id ) AS matches
                FROM Players
                LEFT JOIN Matches win ON Players.id = win.winner
                LEFT JOIN Matches loss ON Players.id = loss.loser
                GROUP BY Players.id, Players.name
                """
        )
        rows = cur.fetchall()

        return rows

    except psycopg2.DatabaseError, e:

        if conn:
            conn.rollback()

        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()

    return []


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = None

    try:
        conn = connect()
        cur = conn.cursor()

        cur.execute("""INSERT INTO Matches (winner, loser) VALUES(%s,%s);""",
                    (winner, loser,))

        conn.commit()

    except psycopg2.DatabaseError, e:

        if conn:
            conn.rollback()

        print 'Error {}'.format(e)

    finally:

        if conn:
            conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()

    pairs = []

    i = 0

    while i < len(standings):

        # finding pair
        j = i + 1
        while j < len(standings):
            if standings[i][2] == standings[j][2]:
                # add to list and stop searching
                pairs.append((standings[i][0], standings[i][1],
                              standings[j][0], standings[j][1]))
                standings.remove(standings[j])
                break
            j += 1
        i += 1

    return pairs
