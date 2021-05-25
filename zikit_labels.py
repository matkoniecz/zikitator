import datetime
import roman


def get_closed_labels():
    return ["zakończone - wycofane", "zakończone - poprawione przed wykonaniem zgłoszenia",
    		"zakończone - poprawione przed moim zgłoszeniem",
            "zakończone - duplikat", "zakończone - przeterminowane", "zakończone - sukces - informacja uzyskana",
            "zakończone - podziękowania"] + get_success_labels()


def get_inactive_labels():
    ended = get_closed_labels()
    recently_posted = ["nadane - " + date_label(0), "nadane - " + date_label(-1), "nadane - " + date_label(-2)]
    recently_posted = ["nadane " + date_label(0), "nadane " + date_label(-1), "nadane " + date_label(-2)]
    progressing_without_prodding = ["kontrapas - do mnie", "kontrapas - do ZIKIT"]
    waits_for_fixing_stupid_law = ["przepisy - wąskie przejścia", "przepisy - ruch dwukierunkowy"]
    may_be_active = ["ma działać - " + date_label(x) for x in range(0, 12)] + ["ma działać - " + date_label_year_only(x) for x in range(0, 5)]
    supposed_to_be_fixed_this_year = ["ma działać - " + str(datetime.datetime.now().year)]
    hibernated = ["hibernacja do " + date_label(x) for x in range(1, 12 * 20)]
    inspection_unnecessary = ["do Rady Miasta", "do ZIKIT", "do ZIKIT - kontrapas", "do SM", "do KMR/prasy",
                              "do dzielnicy", "do innych", "do zielone na poziomie", "do mnie - budżet obywatelski",
                              "do ZIKIT - sekcja rowerowa", "brak kasy - łączniki"]

    return ended + recently_posted + progressing_without_prodding + waits_for_fixing_stupid_law + \
           supposed_to_be_fixed_this_year + hibernated + may_be_active + inspection_unnecessary


def get_success_labels():
    return ["zakończone - sukces"]


def get_activating_labels():
    no_longer_hibernating = ["hibernacja do " + date_label(x) for x in range(-100, -1)]
    return ["projekt 99 - do sprawdzenia"] + no_longer_hibernating + ["zakończone - do weryfikacji"]


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

def date_label_year_only(date_delta_in_years):
    now = datetime.datetime.now()
    return str(now.year + date_delta_in_years)
