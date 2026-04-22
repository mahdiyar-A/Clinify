from common.db import db_cursor
from common.phone import normalize_phone


def update_profile(doctor_id, phone, specialty):
    phone = normalize_phone(phone)
    with db_cursor(commit=True) as cur:
        cur.execute(
            'UPDATE "USER" SET phone = %s WHERE user_id = %s',
            (phone, doctor_id),
        )
        cur.execute(
            'UPDATE doctor SET specialty = %s WHERE doctor_id = %s',
            (specialty or None, doctor_id),
        )


def _fmt_time(t):
    # Accepts 'HH:MM' string; returns '9:00 AM' style. Falls back to input on error.
    try:
        h, m = [int(x) for x in t.split(':')[:2]]
        ampm = 'PM' if h >= 12 else 'AM'
        h12 = h % 12 or 12
        return f'{h12}:{m:02d} {ampm}'
    except Exception:
        return t


def _time_str(t):
    # Normalize a time value (string 'HH:MM[:SS]' or time object) to 'HH:MM'.
    s = t.strftime('%H:%M') if hasattr(t, 'strftime') else str(t)
    return s[:5]


def add_availability_slots(doctor_id, days, start_time, end_time):
    if not days:
        raise ValueError('Please select at least one day.')
    if not start_time or not end_time:
        raise ValueError('Please pick both a start and end time.')
    if start_time == end_time:
        raise ValueError(
            f'Start and end time are the same ({_fmt_time(start_time)}). Please choose a range.'
        )
    if start_time > end_time:
        raise ValueError(
            f'End time ({_fmt_time(end_time)}) must be after start time ({_fmt_time(start_time)}).'
        )
    with db_cursor(commit=True) as cur:
        cur.execute(
            '''SELECT day_of_week, start_time, end_time FROM availability
               WHERE doctor_id = %s AND day_of_week = ANY(%s)''',
            (doctor_id, list(days)),
        )
        existing = cur.fetchall()
        for day, ex_start, ex_end in existing:
            ex_s, ex_e = _time_str(ex_start), _time_str(ex_end)
            if start_time == ex_s and end_time == ex_e:
                raise ValueError(
                    f'You already have this exact slot on {day} ({_fmt_time(ex_s)} – {_fmt_time(ex_e)}).'
                )
            if start_time == ex_s:
                raise ValueError(
                    f'You already have a slot starting at {_fmt_time(ex_s)} on {day}.'
                )
            if end_time == ex_e:
                raise ValueError(
                    f'You already have a slot ending at {_fmt_time(ex_e)} on {day}.'
                )
            if start_time < ex_e and end_time > ex_s:
                raise ValueError(
                    f'This overlaps your existing {_fmt_time(ex_s)} – {_fmt_time(ex_e)} slot on {day}.'
                )
        for day in days:
            cur.execute(
                'INSERT INTO availability (doctor_id, day_of_week, start_time, end_time) '
                'VALUES (%s, %s, %s, %s)',
                (doctor_id, day, start_time, end_time),
            )


def delete_availability(doctor_id, day_of_week, start_time):
    with db_cursor(commit=True) as cur:
        cur.execute(
            'DELETE FROM availability '
            'WHERE doctor_id = %s AND day_of_week = %s AND start_time = %s',
            (doctor_id, day_of_week, start_time),
        )


def record_visit(doctor_id, patient_id, appointment_id, diagnosis, vitals, notes):
    if not appointment_id:
        raise ValueError('Please select an appointment.')
    with db_cursor(commit=True) as cur:
        cur.execute(
            '''SELECT 1 FROM appointment
               WHERE appointment_id = %s AND patient_id = %s
                 AND doctor_id = %s AND status = 'Scheduled' ''',
            (appointment_id, patient_id, doctor_id),
        )
        if not cur.fetchone():
            raise ValueError('You can only record visits for your own scheduled appointments.')
        cur.execute(
            'SELECT create_visit(%s, %s, %s, %s, %s, %s)',
            (int(appointment_id), int(patient_id), 1, diagnosis, vitals, notes),
        )


def _assert_doctor_owns_appointment(cur, doctor_id, appointment_id, require_scheduled=True):
    sql = 'SELECT 1 FROM appointment WHERE appointment_id = %s AND doctor_id = %s'
    params = [appointment_id, doctor_id]
    if require_scheduled:
        sql += " AND status = 'Scheduled'"
    cur.execute(sql, params)
    if not cur.fetchone():
        raise ValueError('Appointment not found or not actionable.')


def cancel_appointment(doctor_id, appointment_id):
    with db_cursor(commit=True) as cur:
        _assert_doctor_owns_appointment(cur, doctor_id, appointment_id)
        cur.execute('SELECT cancel_appointment(%s)', (int(appointment_id),))


def mark_no_show(doctor_id, appointment_id):
    with db_cursor(commit=True) as cur:
        _assert_doctor_owns_appointment(cur, doctor_id, appointment_id)
        cur.execute(
            "UPDATE appointment SET status = 'No-Show' WHERE appointment_id = %s",
            (int(appointment_id),),
        )


def update_visit(doctor_id, appointment_id, diagnosis, vitals, notes):
    with db_cursor(commit=True) as cur:
        cur.execute(
            '''SELECT 1 FROM visit v
               JOIN appointment a ON v.appointment_id = a.appointment_id
               WHERE v.appointment_id = %s AND a.doctor_id = %s''',
            (appointment_id, doctor_id),
        )
        if not cur.fetchone():
            raise ValueError('Visit not found.')
        cur.execute(
            '''UPDATE visit SET diagnosis = %s, vitals = %s, visit_notes = %s
               WHERE appointment_id = %s''',
            (diagnosis, vitals, notes, appointment_id),
        )


def create_prescription(doctor_id, visit_id, medication_ids, frequencies, durations):
    with db_cursor(commit=True) as cur:
        cur.execute('SELECT create_prescription(%s, %s)', (visit_id, doctor_id))
        prescription_id = cur.fetchone()[0]
        for med_id, freq, dur in zip(medication_ids, frequencies, durations):
            cur.execute(
                'INSERT INTO contains VALUES (%s, %s, %s, %s)',
                (prescription_id, med_id, freq, dur),
            )
    return prescription_id
