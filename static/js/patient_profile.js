(function () {
    var form = document.querySelector('.profile-wrap form');
    if (!form) return;

    var MONTHS = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December'];

    function toISODate(d) {
        return d.getFullYear() + '-' +
            String(d.getMonth() + 1).padStart(2, '0') + '-' +
            String(d.getDate()).padStart(2, '0');
    }

    function fmtDisplayDate(iso) {
        if (!iso) return '';
        var d = new Date(iso + 'T00:00:00');
        return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    }

    // ---- Popover manager ----
    var openPop = null;
    function closeAnyPop() {
        if (openPop) { openPop.hidden = true; openPop = null; }
    }
    document.addEventListener('click', function (e) {
        if (!openPop) return;
        if (!e.target.closest('[data-cp-pop]') && !e.target.closest('[data-cp-trigger]')) {
            closeAnyPop();
        }
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeAnyPop();
    });
    function togglePop(pop) {
        if (openPop && openPop !== pop) openPop.hidden = true;
        pop.hidden = !pop.hidden;
        openPop = pop.hidden ? null : pop;
    }

    function flashHint(el, message) {
        var existing = el.querySelector('.inline-hint');
        if (existing) existing.remove();
        var hint = document.createElement('div');
        hint.className = 'inline-hint';
        hint.textContent = message;
        el.appendChild(hint);
        setTimeout(function () { hint.remove(); }, 3500);
    }

    // ---- Gender picker ----
    function initGenderPicker() {
        var root = document.getElementById('gender-picker');
        if (!root) return null;
        var input = root.querySelector('#gender-input');
        var trigger = root.querySelector('#gender-trigger');
        var display = root.querySelector('.cp-display');
        var pop = root.querySelector('[data-cp-pop]');
        var list = root.querySelector('[data-gender-list]');
        var options = ['Male', 'Female', 'Other'];

        options.forEach(function (v) {
            var opt = document.createElement('button');
            opt.type = 'button';
            opt.className = 'cp-option';
            opt.dataset.value = v;
            opt.textContent = v;
            list.appendChild(opt);
        });

        function setValue(v) {
            input.value = v || '';
            display.textContent = v || 'Select gender';
            trigger.classList.toggle('has-value', !!v);
            list.querySelectorAll('.cp-option.is-active').forEach(function (b) {
                b.classList.remove('is-active');
            });
            var active = list.querySelector('.cp-option[data-value="' + v + '"]');
            if (active) active.classList.add('is-active');
        }

        list.addEventListener('click', function (e) {
            var opt = e.target.closest('.cp-option');
            if (!opt) return;
            setValue(opt.dataset.value);
            closeAnyPop();
        });

        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            togglePop(pop);
        });

        setValue(input.value);
        return { getValue: function () { return input.value; } };
    }

    // ---- DOB picker ----
    function initDobPicker() {
        var root = document.getElementById('dob-picker');
        if (!root) return null;
        var input = root.querySelector('#dob-input');
        var trigger = root.querySelector('#dob-trigger');
        var display = root.querySelector('.cp-display');
        var pop = root.querySelector('[data-cp-pop]');
        var grid = root.querySelector('[data-cal-grid]');
        var label = root.querySelector('[data-cal-label]');
        var prev = root.querySelector('[data-cal-prev]');
        var next = root.querySelector('[data-cal-next]');
        var yearTrigger = root.querySelector('[data-cal-year-trigger]');
        var yearPop = root.querySelector('[data-cal-year-pop]');
        var yearList = root.querySelector('[data-cal-year-list]');

        var today = new Date();
        today.setHours(0, 0, 0, 0);
        var minYear = today.getFullYear() - 120;
        var minDate = new Date(minYear, 0, 1);
        var maxDate = today;

        var viewDate = new Date();
        viewDate.setDate(1);
        viewDate.setHours(0, 0, 0, 0);
        if (input.value) {
            var init = new Date(input.value + 'T00:00:00');
            if (!isNaN(init)) {
                viewDate = new Date(init.getFullYear(), init.getMonth(), 1);
            }
        } else {
            viewDate = new Date(today.getFullYear(), today.getMonth(), 1);
        }

        function renderYears() {
            yearList.innerHTML = '';
            for (var y = maxDate.getFullYear(); y >= minYear; y--) {
                var b = document.createElement('button');
                b.type = 'button';
                b.className = 'cal-year';
                b.dataset.year = String(y);
                b.textContent = String(y);
                if (y === viewDate.getFullYear()) b.classList.add('is-active');
                yearList.appendChild(b);
            }
        }

        function clampView() {
            var minMonth = new Date(minDate.getFullYear(), minDate.getMonth(), 1);
            var maxMonth = new Date(maxDate.getFullYear(), maxDate.getMonth(), 1);
            if (viewDate < minMonth) viewDate = minMonth;
            if (viewDate > maxMonth) viewDate = maxMonth;
        }

        function canGo(dir) {
            var probe = new Date(viewDate);
            probe.setMonth(probe.getMonth() + dir);
            var minMonth = new Date(minDate.getFullYear(), minDate.getMonth(), 1);
            var maxMonth = new Date(maxDate.getFullYear(), maxDate.getMonth(), 1);
            if (probe < minMonth) return false;
            if (probe > maxMonth) return false;
            return true;
        }

        function render() {
            clampView();
            grid.innerHTML = '';
            label.textContent = MONTHS[viewDate.getMonth()] + ' ' + viewDate.getFullYear();

            var first = new Date(viewDate);
            var startWd = first.getDay();
            var daysInMonth = new Date(viewDate.getFullYear(), viewDate.getMonth() + 1, 0).getDate();

            for (var i = 0; i < startWd; i++) {
                var pad = document.createElement('span');
                pad.className = 'cal-day cal-day--pad';
                grid.appendChild(pad);
            }

            for (var d = 1; d <= daysInMonth; d++) {
                var date = new Date(viewDate.getFullYear(), viewDate.getMonth(), d);
                var iso = toISODate(date);
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'cal-day';
                btn.textContent = String(d);
                btn.dataset.date = iso;

                var inRange = date >= minDate && date <= maxDate;
                if (!inRange) {
                    btn.disabled = true;
                    btn.classList.add('is-disabled');
                }
                if (toISODate(date) === toISODate(today)) btn.classList.add('is-today');
                if (input.value === iso) btn.classList.add('is-selected');
                grid.appendChild(btn);
            }
        }

        function setValue(iso) {
            input.value = iso || '';
            display.textContent = iso ? fmtDisplayDate(iso) : 'Select date of birth';
            trigger.classList.toggle('has-value', !!iso);
        }

        // Initialize display from existing value
        if (input.value) setValue(input.value);

        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            if (pop.hidden) render();
            togglePop(pop);
        });

        prev.addEventListener('click', function (e) {
            e.stopPropagation();
            if (!canGo(-1)) return;
            viewDate.setMonth(viewDate.getMonth() - 1);
            render();
        });
        next.addEventListener('click', function (e) {
            e.stopPropagation();
            if (!canGo(1)) return;
            viewDate.setMonth(viewDate.getMonth() + 1);
            render();
        });

        grid.addEventListener('click', function (e) {
            var day = e.target.closest('.cal-day');
            if (!day || day.disabled) return;
            setValue(day.dataset.date);
            grid.querySelectorAll('.cal-day.is-selected').forEach(function (b) {
                b.classList.remove('is-selected');
            });
            day.classList.add('is-selected');
            closeAnyPop();
        });

        yearTrigger.addEventListener('click', function (e) {
            e.stopPropagation();
            if (yearPop.hidden) renderYears();
            yearPop.hidden = !yearPop.hidden;
        });

        yearList.addEventListener('click', function (e) {
            var b = e.target.closest('.cal-year');
            if (!b) return;
            viewDate.setFullYear(Number(b.dataset.year));
            viewDate.setMonth(viewDate.getMonth());
            yearPop.hidden = true;
            render();
        });

        pop.addEventListener('click', function (e) {
            // Don't close outer pop when interacting inside year pop
            if (e.target.closest('[data-cal-year-pop]')) e.stopPropagation();
        });

        return { getValue: function () { return input.value; } };
    }

    var genderPicker = initGenderPicker();
    var dobPicker = initDobPicker();

    form.addEventListener('submit', function (e) {
        var ok = true;
        var dobRoot = document.getElementById('dob-picker');
        var genderRoot = document.getElementById('gender-picker');

        if (dobPicker && !dobPicker.getValue()) {
            ok = false;
            flashHint(dobRoot, 'Please select your date of birth.');
        }
        if (genderPicker && !genderPicker.getValue()) {
            ok = false;
            flashHint(genderRoot, 'Please select your gender.');
        }
        if (!ok) e.preventDefault();
    });
})();

