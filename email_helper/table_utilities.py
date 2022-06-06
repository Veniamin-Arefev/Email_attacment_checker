import datetime
import os

from bs4 import BeautifulSoup as Soup

__all__ = ['create_html']

import email_helper.deadlines


def create_html_from_database(target_path, target_filename):
    import database
    from database.models import Student, Task, Report

    session = database.session_factory()
    with open('email_helper' + os.sep + 'pattern.php', 'r', encoding='utf-8') as in_file:
        soup = Soup(in_file, features='html.parser')

        table = soup.find('table')
        table.append(thead := soup.new_tag('thead'))
        table.append(tbody := soup.new_tag('tbody'))

        thead.append(head_tr := soup.new_tag('tr'))
        # thead content

        mails = [item[0] for item in session.query(Student.email)]

        for i in ['Username', 'Email', *email_helper.deadlines.homeworks_names_and_files.keys(), 'Total\xa0grade']:
            elem = soup.new_tag('th', attrs={'scope': 'col'})
            elem.string = i
            head_tr.append(elem)

        for cur_email in mails:
            tbody.append(body_tr := soup.new_tag('tr'))

            elem = soup.new_tag('th')
            elem.string = session.query(Student.name).filter(Student.email == cur_email).first()[0].replace(' ',
                                                                                                            u'\xa0')
            body_tr.append(elem)

            elem = soup.new_tag('th')
            name, domain = cur_email.split('@')
            elem.string = f'{name[:3]}*@{domain}'
            body_tr.append(elem)

            submitted_tasks = {key: value for key, *value in
                               session.query(Task.name, Task.creation_date, Task.grade).join(Student).filter(
                                   Student.email == cur_email)}

            for homework_name in email_helper.deadlines.homeworks_names_and_files.keys():
                if homework_name in submitted_tasks.keys():
                    color = None
                    if submitted_tasks[homework_name][1] == 4:
                        color = 'bg-success'
                    elif submitted_tasks[homework_name][1] == 2:
                        color = 'bg-warning'
                    elif submitted_tasks[homework_name][1] == 1:
                        color = 'bg-danger'
                    elif submitted_tasks[homework_name][1] == 0:  # not original
                        color = 'bg-primary'
                    else:
                        color = 'bg-info'
                    elem = soup.new_tag('th', attrs={'class': color})
                    elem.string = submitted_tasks[homework_name][0].strftime("%d\xa0%b\xa0%H:%M")
                else:
                    elem = soup.new_tag('th')
                    elem.string = 'Nope'
                body_tr.append(elem)
            elem = soup.new_tag('th')
            elem.string = str(sum([item[1] for item in submitted_tasks.values()]))
            body_tr.append(elem)

        soup.find('h6').string = f'Last updated: {datetime.datetime.now().strftime("%d %b %H:%M")}'. \
            replace(' ', u'\xa0')
        with open(target_path + os.sep + target_filename, 'w', encoding='utf-8') as out_file:
            out_file.write(str(soup).replace('&gt;', '>'))

    session.close()
    with open('email_helper' + os.sep + 'data.php', 'r', encoding='utf-8') as in_file:
        with open(target_path + os.sep + 'data.php', 'w', encoding='utf-8') as out_file:
            out_file.write(in_file.read())


def create_html(emails_dict: dict, mailer_names: dict, target_path, target_filename):
    mailer_names = dict(sorted(mailer_names.items(), key=lambda x: x[1]))

    unique_emails = list(mailer_names.keys())

    with open('email_helper' + os.sep + 'pattern.php', 'r', encoding='utf-8') as file:
        soup = Soup(file, features='html.parser')

        table = soup.find('table')
        table.append(thead := soup.new_tag('thead'))
        table.append(tbody := soup.new_tag('tbody'))

        thead.append(head_tr := soup.new_tag('tr'))
        # thead content
        for i in ['Username', 'Email', *emails_dict]:
            elem = soup.new_tag('th', attrs={'scope': 'col'})
            elem.string = i
            head_tr.append(elem)

        for cur_email in unique_emails:
            tbody.append(body_tr := soup.new_tag('tr'))

            elem = soup.new_tag('th')
            elem.string = mailer_names[cur_email].replace(' ', u'\xa0')
            body_tr.append(elem)

            elem = soup.new_tag('th')
            name, domain = cur_email.split('@')
            elem.string = f'{name[:3]}*@{domain}'
            body_tr.append(elem)

            for item in [*emails_dict.values()]:
                # should be more correct handling
                # correct submitted task
                all_tries = list(filter(lambda x: cur_email in x, item))
                if all_tries:
                    task_info = max(all_tries, key=lambda x: x[2])
                    elem = soup.new_tag('th', attrs={'class': 'bg-success' if task_info[3] else 'bg-danger'})
                    elem.string = task_info[2].strftime("%d\xa0%b\xa0%H:%M")
                else:
                    elem = soup.new_tag('th')
                    elem.string = 'Nope'
                body_tr.append(elem)

        soup.find('h6').string = f'Last updated: {datetime.datetime.now().strftime("%d %b %H:%M")}'.replace(' ',
                                                                                                            u'\xa0')
        with open(target_path + os.sep + target_filename, 'w', encoding='utf-8') as file1:
            file1.write(str(soup).replace('&gt;', '>'))
    with open('email_helper' + os.sep + 'data.php', 'r', encoding='utf-8') as in_file:
        with open(target_path + os.sep + 'data.php', 'w', encoding='utf-8') as out_file:
            out_file.write(in_file.read())
