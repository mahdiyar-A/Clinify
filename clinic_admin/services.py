from django.contrib.auth.hashers import make_password

from accounts import selectors as account_selectors
from common.db import db_cursor
from common.names import normalize_person_name
from common.phone import normalize_phone

from . import selectors


def create_admin(data):
    """Create an additional admin account. Email domain is enforced by the form."""
    if account_selectors.email_exists(data['email']):
        raise ValueError('An account with this email already exists.')

    first_name = normalize_person_name(data['first_name'])
    last_name = normalize_person_name(data['last_name'])
    password_hash = make_password(data['password'])
    with db_cursor(commit=True) as cur:
        cur.execute(
            '''INSERT INTO "USER" (first_name, last_name, email, password_hash, role)
               VALUES (%s, %s, %s, %s, 'admin') RETURNING user_id''',
            (first_name, last_name, data['email'], password_hash),
        )
        user_id = cur.fetchone()[0]
        cur.execute('INSERT INTO admin (admin_id) VALUES (%s)', (user_id,))
    return user_id


def cancel_appointment(appointment_id):
    with db_cursor(commit=True) as cur:
        cur.execute('SELECT cancel_appointment(%s)', (appointment_id,))


def update_appointment_status(appointment_id, status):
    with db_cursor(commit=True) as cur:
        cur.execute(
            'UPDATE appointment SET status = %s WHERE appointment_id = %s',
            (status, appointment_id),
        )


def update_user(user_id, first_name, last_name, phone, new_role):
    """Update a user's name and phone. Role changes are not permitted here."""
    current_role = selectors.get_user_role(user_id)
    if current_role and current_role != new_role:
        raise ValueError(
            f'Role change not allowed. User is currently a {current_role}. '
            'Delete and re-create the account to change roles.'
        )
    phone = normalize_phone(phone)
    with db_cursor(commit=True) as cur:
        cur.execute(
            'UPDATE "USER" SET first_name=%s, last_name=%s, phone=%s WHERE user_id=%s',
            (first_name, last_name, phone, user_id),
        )


def delete_user(user_id):
    with db_cursor(commit=True) as cur:
        cur.execute('DELETE FROM "USER" WHERE user_id = %s', (user_id,))


def add_medication(name, description, dosage_form):
    with db_cursor(commit=True) as cur:
        cur.execute(
            'INSERT INTO medication (medication_name, description, dosage_form) '
            'VALUES (%s, %s, %s)',
            (name, description, dosage_form),
        )


def delete_medication(medication_id):
    with db_cursor(commit=True) as cur:
        cur.execute(
            'DELETE FROM medication WHERE medication_id = %s',
            (medication_id,),
        )
