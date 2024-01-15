import PySimpleGUI as sg
from logic import doctor_queue_logic as logic


def clear_all_fields(window):
    window['-IN_NAME-']('')
    window['-IN_SURNAME-']('')
    window['-IN_PESEL-']('')
    window['-IN_AGE-'](0)
    # window['-IN_SEX-']('')
    window['M'](True)
    window['F'](False)
    window['N'](False)
    
    window['-IN_IS_PRIORITY-'](False)
    window['-IN_PLACE-'](1)
    window['-IN_PLACE-'].update(visible=False)
    window['-IN_REMOVE_PATIENT-'](1)

def update_list_dependant_fields(window):
    window['-OUT_LIST-'].update(str(patient_list))
    window['-IN_PLACE-'].update(range=(1, 1 if not patient_list.Length() else patient_list.Length()))
    window['-IN_REMOVE_PATIENT-'].update(range=(1, 1 if not patient_list.Length() else patient_list.Length()))

def change_layout_to(window, new_layout_key):
    window['-ADD_PATIENT-'].update(visible=False)
    window['-REMOVE_PATIENT-'].update(visible=False)
    window['-MAIN-'].update(visible=False)

    window[new_layout_key].update(visible=True)

def get_gender_choice(values):
    if values['F']:
        return 'F'
    elif values['M']:
        return 'M'
    elif values['N']:
        return 'N'
    else:
        raise Exception('Program nie zapewnia tego')

patient_list = logic.List()

sg.theme('DarkAmber')

layout1 = [
    [sg.Text('Kolejka')],
    [sg.Text(str(patient_list), key='-OUT_LIST-')],
    [sg.Button('Dodaj pacjenta'), sg.Button('Usuń pacjenta'), sg.Button('Zamknij'),],
]

layout2 = [
    [sg.Text('Dodaj nowego pacjenta')],
    [sg.Text('Imie'), sg.Input(key='-IN_NAME-')],
    [sg.Text('Nazwisko'), sg.Input(key='-IN_SURNAME-')],
    [sg.Text('Pesel'), sg.Input(key='-IN_PESEL-')],
    [sg.Text('Wiek'), sg.Slider(range=(0, 100), orientation='h', key='-IN_AGE-')],
    [sg.Text('Plec'), sg.Radio("Chłop", "gen", key='M', default=True), sg.Radio("Baba", "gen", key='F'), sg.Radio("Nie wiem", "gen", key='N')],
    [sg.Checkbox('Czy jest priorytetowym?', key='-IN_IS_PRIORITY-', enable_events=True, default=False)],
    [sg.Text('Wybierz mejsce', key='-IN_PLACE_LABEL-', visible=False), sg.Slider(range=(1, 1 if not patient_list.Length() else patient_list.Length()), orientation='h', key='-IN_PLACE-', visible=False)],
    [sg.Button('Zatwerdź'), sg.Button('Powrót do widoku głównego', key='-RETURN_TO_MAIN-')],
]

layout3 = [
    [sg.Text('Usun pacjenta po numeru:')],
    [sg.Slider(range=(1, 1 if not patient_list.Length() else patient_list.Length()), orientation='h', key='-IN_REMOVE_PATIENT-')],
    [sg.Button('Usuń'), sg.Button('Powrót do widoku głównego')],
]

layout = [
    [sg.Column(layout1, key='-MAIN-'), sg.Column(layout2, visible=False, key='-ADD_PATIENT-'), sg.Column(layout3, visible=False, key='-REMOVE_PATIENT-')]
]

window = sg.Window('Kolejka do doktora', layout)


while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Zamknij'):
        break

    if event == '-IN_IS_PRIORITY-' and values['-IN_IS_PRIORITY-']:
        if not patient_list.CzyKtosZnajdujeSieWKolejce():
            sg.popup_ok('Nie możesz dodawać pacjenta priorytetowego poki nie dodasz jednego')
            window['-IN_IS_PRIORITY-'](False)
            # window['-IN_PLACE_LABEL-'](False)

            continue

        print(values['-IN_IS_PRIORITY-'])
        window['-IN_PLACE-'].update(visible=True)
        window['-IN_PLACE_LABEL-'].update(visible=True)

    
    elif event == '-IN_IS_PRIORITY-' and not values['-IN_IS_PRIORITY-']:
        window['-IN_PLACE-'].update(visible=False)
        window['-IN_PLACE_LABEL-'].update(visible=False)

    elif event == 'Zatwerdź':
        name = values['-IN_NAME-']
        surname = values['-IN_SURNAME-']
        pesel = values['-IN_PESEL-']
        age = int(values['-IN_AGE-'])
        # sex = values['-IN_SEX-']
        sex = get_gender_choice(values)
        is_priority = values['-IN_IS_PRIORITY-']
        place = values['-IN_PLACE-']

        try:
            if is_priority:
                patient_list.dodajPacjentaPriorytetowego(place, name, surname, pesel, age, sex)
            else:
                patient_list.dodajPacjenta(name, surname, pesel, age, sex)
        except Exception as e:
            sg.popup_ok(e)
            continue
        
        clear_all_fields(window)

        update_list_dependant_fields(window)
        change_layout_to(window, '-MAIN-')

    elif event == "Usuń":
        place = values['-IN_REMOVE_PATIENT-']
        patient_list.UsunPacjenta(place)

        window['-IN_REMOVE_PATIENT-'](1)

        update_list_dependant_fields(window)
        change_layout_to(window, '-MAIN-')

    elif event == 'Powrót do widoku głównego' or event == '-RETURN_TO_MAIN-':
        change_layout_to(window, '-MAIN-')
        clear_all_fields(window)

    elif event == 'Dodaj pacjenta':
        change_layout_to(window, '-ADD_PATIENT-')

    elif event == 'Usuń pacjenta':
        if not patient_list.CzyKtosZnajdujeSieWKolejce():
            sg.popup_ok('Nie możesz usuwać pacjenta poki nie dodasz jednego')
            continue
        change_layout_to(window, '-REMOVE_PATIENT-')

    elif event == 'Usuń':
        numer_pacjenta = window['-IN_REMOVE_PATIENT-']
        clear_all_fields(window)
        change_layout_to(window, '-MAIN-')


window.close()
