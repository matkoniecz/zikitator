import datetime
import roman


def get_closed_labels():
    return ["zakończone - sukces", "zakończone - wycofane", "zakończone - poprawione przed wykonaniem zgłoszenia",
            "zakończone - duplikat", "zakończone - przeterminowane"]


def get_inactive_labels():
    ended = get_closed_labels()
    recently_posted = ["nadane " + date_label(0), "nadane " + date_label(-1)]
    progressing_without_prodding = ["kontrapas - do mnie", "kontrapas - do ZIKIT"]
    waits_for_fixing_stupid_law = ["przepisy - wąskie przejścia", "przepisy - ruch dwukierunkowy"]
    may_be_active = ["ma działać - " + date_label(x) for x in range(0, 12)]
    supposed_to_be_fixed_this_year = ["ma działać - " + str(datetime.datetime.now().year)]
    hibernated = ["hibernacja do " + date_label(x) for x in range(1, 12*5)]
    inspection_unnecessary = ["do Rady Miasta", "do ZIKIT", "do ZIKIT - kontrapas", "do SM", "do KMR/prasy",
                              "do dzielnicy", "do innych", "do zielone na poziomie", "do mnie - budżet obywatelski",
                              "brak kasy - łączniki"]

    return ended + recently_posted + progressing_without_prodding + waits_for_fixing_stupid_law + \
           supposed_to_be_fixed_this_year + hibernated + may_be_active + inspection_unnecessary


def get_success_labels():
    return ["zakończone - sukces"]


def get_activating_labels():
    hibernating = ["hibernacja do " + date_label(x) for x in range(-100, -1)]
    return ["projekt 99 - do sprawdzenia"] + hibernating + ["zakończone - do weryfikacji"]


def get_labels_marking_unlocatable():
    return ["bez lokalizacji"]


def date_label(date_delta_in_months):
    now = datetime.datetime.now()
    year = now.year
    month = now.month + date_delta_in_months
    while month > 12:
        year += 1
        month -= 12
    while month <= 0:
        year -= 1
        month += 12
    return str(year) + " " + roman.toRoman(month)
