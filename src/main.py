import PySimpleGUI as sg
from logic import doctor_queue_logic as logic

patient_list = logic.List()

sg.theme('DarkAmber')   # Add a touch of color
# ----------- Create the 3 layouts this Window will display -----------

layout1 = [
    [sg.Text('Kolejka')],
    [sg.Text(str(patient_list), key='-OUT_LIST-')],
    [sg.Button('Dodaj pacjenta'), sg.Button('Zamknij')]
]

layout2 = [
    [sg.Text('Dodaj nowego pacjenta')],
    [sg.Text('Imie'), sg.Input(key='-IN_NAME-')],
    [sg.Text('Nazwisko'), sg.Input(key='-IN_SURNAME-')],
    [sg.Text('Pesel'), sg.Input(key='-IN_PESEL-')],
    [sg.Text('Wiek'), sg.Slider(range=(0, 100), orientation='h', key='-IN_AGE-')],
    [sg.Text('Plec'), sg.Input(key='-IN_SEX-')],
    [sg.Checkbox('Czy jest priorytetowym?', key='-IN_IS_PRIORITY-')],
    [sg.Button('Zatwerdź'), sg.Button('Powrót do widoku głównego')],
]


# ----------- Create actual layout using Columns and a row of Buttons
layout = [
    [sg.Column(layout1, key='-MAIN-'), sg.Column(layout2, visible=False, key='-ADD_PATIENT-')]
]

window = sg.Window('Swapping the contents of a window', layout)

layout = 1  # The currently visible layout


while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Zamknij'):
        break

    if event == 'Zatwerdź':
        name = values['-IN_NAME-']
        surname = values['-IN_SURNAME-']
        pesel = values['-IN_PESEL-']
        age = int(values['-IN_AGE-'])
        sex = values['-IN_SEX-']

        window['-IN_NAME-']('')
        window['-IN_SURNAME-']('')
        window['-IN_PESEL-']('')
        window['-IN_AGE-'](0)
        window['-IN_SEX-']('')

        patient_list.dodajPacjenta(name, surname, pesel, age, sex)
        
        window['-OUT_LIST-'].update(str(patient_list))

        window[f'-ADD_PATIENT-'].update(visible=False)
        window[f'-MAIN-'].update(visible=True)

    elif event == 'Powrót do widoku głównego':
        window[f'-ADD_PATIENT-'].update(visible=False)
        window[f'-MAIN-'].update(visible=True)

    elif event == 'Dodaj pacjenta':
        window[f'-MAIN-'].update(visible=False)
        window[f'-ADD_PATIENT-'].update(visible=True)
window.close()
