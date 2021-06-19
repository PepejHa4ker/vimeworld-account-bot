from util import database


def parse(filename):
    with open(filename) as file:
        lines = file.read()

        lines = lines.split('\n')

        for line in lines:
            content = line.split('\t')

            print(str(content))

            timestamp = datetime.fromtimestamp(int(content[9]))

            database.run_sql(
                """
                INSERT INTO public.users (id, login, password, password_version, email, reg_time) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (content[0], content[1], content[2], content[3], content[8], timestamp.strftime('%Y/%m/%d-%H:%M:%S'))
            )


def parse_oauth(filename):
    with open(filename) as file:
        lines = file.read()

        lines = lines.split('\n')

        for line in lines:
            content = line.split('\t')

            print(str(content))

            if content[1] == 'totp':
                continue

            database.run_sql(
                """
                INSERT INTO public.oauth (id, keys) 
                VALUES (%s, %s)
                """,
                (content[0], content[2])
            )


if __name__ == "__main__":
    parse("VimeWorld.txt")
    parse_oauth("Oauth.txt")
