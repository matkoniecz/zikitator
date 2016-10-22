import zikit_labels

def show(function):
	print("\n")
	print(function.__name__)
	print(function())

show(zikit_labels.get_closed_labels)
show(zikit_labels.get_inactive_labels)
show(zikit_labels.get_success_labels)
show(zikit_labels.get_activating_labels)
show(zikit_labels.get_labels_marking_unlocatable)