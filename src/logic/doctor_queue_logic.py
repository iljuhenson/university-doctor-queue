from datetime import datetime

class Node():
    def __init__(self, imie = None, nazwisko = None, pesel = None, wiek = None, plec = None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.wiek = wiek
        self.plec = plec
        self.godzina = datetime.now().strftime("%H:%M:%S")
        self.next = None


class List():
    def __init__(self):
        self.head = Node()

    def dodajPacjenta(self, imie, nazwisko, pesel, wiek, plec):
        appended_node = Node(imie, nazwisko, pesel, wiek, plec)
        if self.head.pesel is None:
            self.head = appended_node
        else:
            counter = self.head
            while counter.next is not None:
                counter = counter.next
            counter.next = appended_node

    def dodajPacjentaPriorytetowego(self, miejsce, imie, nazwisko, pesel, wiek, plec):
        if miejsce < 1:
            print("Numeracja miejsc zaczyna się od 1")
            return
        if miejsce > self.Length():
            print("Nie ma tylu pacjentów, pacjent dodany na ostatnie miejsce")
            self.dodajPacjenta(imie, nazwisko, pesel, wiek, plec)
            return

        appended_node = Node(imie, nazwisko, pesel, wiek, plec)
        counter = self.head
        previous = None
        i = 1
        while counter.next is not None and i < miejsce:
            previous = counter
            counter = counter.next
            i += 1
        if previous is not None:
            previous.next = appended_node
            appended_node.next = counter
        else:
            self.head = appended_node
            appended_node.next = counter


    def Wyswietl(self):
        if self.head.pesel is None:
            print("Lista pacjentów jest pusta")
            return
        print("Lista pacjentów:")
        counter = self.head
        i = 1
        dlugosc = self.Length()
        while i <= dlugosc:
            print(i, ":", counter.imie, counter.nazwisko, "PESEL:", counter.pesel, "wiek:", counter.wiek, counter.plec, "przyjęty/a:", counter.godzina)
            counter = counter.next
            i += 1

    def __str__(self):
        ret_str = ''

        if self.head.pesel is None:
            return "Lista pacjentów jest pusta"

        
        counter = self.head
        i = 1
        dlugosc = self.Length()
        while i <= dlugosc:
            ret_str += f"{i}: {counter.imie} {counter.nazwisko} PESEL: {counter.pesel} wiek: {counter.wiek} plec: {counter.plec} przyjęty/a: {counter.godzina}\n"
            
            counter = counter.next
            i += 1

        return ret_str

    def Length(self):
        if self.head.pesel is None:
            return 0
        else:
            i = 1
            counter = self.head
            while counter.next is not None:
                counter = counter.next
                i += 1
            return i

    def UsunPacjenta(self, miejsce):
        if self.head.pesel is None:
            print("Lista pacjentów jest pusta")
            return
        dlugosc = self.Length()
        if 1 > miejsce or miejsce > dlugosc:
            print("Nie ma pacjenta na takim miejscu")
            return
        i = 1
        previous = None
        counter = self.head
        while i < miejsce:
            i += 1
            previous = counter
            counter = counter.next
        if previous is not None:
            previous.next = counter.next
        else:
            self.head = counter.next


if __name__ == "__main__":
    pacjenci = List()
    pacjenci.dodajPacjenta("Szymon", "Mlonek", "123", 21, "M")
    pacjenci.dodajPacjenta("Ilya", "Pauliuk", "321", 20, "K")
    pacjenci.dodajPacjentaPriorytetowego(2, "Szymon2", "Mlonek", "123123", 12, "M")
    pacjenci.Wyswietl()
    pacjenci.UsunPacjenta(2)
    pacjenci.Wyswietl()