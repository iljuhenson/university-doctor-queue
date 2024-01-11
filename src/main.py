import PySimpleGUI as sg
from logic import doctor_queue_logic as logic

sg.theme('DarkAmber')   # Add a touch of color
# ----------- Create the 3 layouts this Window will display -----------
layout1 = [
    
]

layout2 = [
    [sg.Text('Dodaj nowego pacjenta')],
    [sg.Text('Imie'), sg.Input(key='-IN_NAME-')],
    [sg.Text('Nazwisko'), sg.Input(key='-IN_SURNAME-')],
    [sg.Text('Pesel'), sg.Input(key='-IN_PESEL-')],
    [sg.Text('Wiek'), sg.Slider(range=(0, 100), orientation='h', key='-IN_AGE-')],
    [sg.Text('Imie'), sg.Input(key='-IN_SEX-')],
    [sg.Checkbox('Czy jest priorytetowym?', key='-IN_IS_PRIORITY-')],
    [sg.Button('Dodaj pacjenta'), sg.Button('Powrót do widoku głównego')],
]

layout3 = [[sg.Text('Kolejka')],
           *[[sg.R(f'Radio {i}', 1)] for i in range(8)]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-MAIN-'), sg.Column(layout2, visible=False, key='-ADD_PATIENT-'), sg.Column(layout3, visible=False, key='-COL3-')],
          [sg.Button('Cycle Layout'), sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('Exit')]]

window = sg.Window('Swapping the contents of a window', layout)

layout = 1  # The currently visible layout

patient_list = logic.List()

while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    # if event == 'Cycle Layout':
    #     window[f'-COL{layout}-'].update(visible=False)
    #     layout = layout + 1 if layout < 3 else 1
    #     window[f'-COL{layout}-'].update(visible=True)
    # elif event in '123':
    #     window[f'-COL{layout}-'].update(visible=False)
    #     layout = int(event)
    #     window[f'-COL{layout}-'].update(visible=True)
    if event == 'Zatwerdź':
        name = values['-IN_NAME-']
        surname = values['-IN_SURNAME-']
        pesel = values['-IN_PESEL-']
        age = int(values['-IN_AGE-'])
        sex = values['-IN_SEX-']

        patient_list.dodajPacjenta(imie, nazwisko, pesel, wiek, sex)

    elif event == 'Powrót do widoku głównego':
        window[f'-ADD_PATIENT-'].update(visible=False)
        layout = int(event)
        window[f'-MAIN-'].update(visible=True)
window.close()
