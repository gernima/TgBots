bot_cost = 4.5
bot_plus_per_day = 0.4
stats = {'day': 0, 'bots': 13, 'plus': 0, 'balance': 0, 'bots_later': {}}
days = 90
for day in range(1, days + 1, 1):
	stats['day'] = day
	stats['plus'] = stats['bots'] * bot_plus_per_day
	stats['balance'] += stats['plus']
	while stats['balance'] >= bot_cost:
		stats['balance'] -= bot_cost
		if day + 7 in stats['bots_later']:
			stats['bots_later'][day + 7] += 1
		else:
			stats['bots_later'][day + 7] = 1
	a = stats['bots_later'].copy()
	for bot_day in a:
		while bot_day in stats['bots_later'] and bot_day <= day:
			stats['bots'] += 1
			if stats['bots_later'][bot_day] - 1 != 0:
				stats['bots_later'][bot_day] -= 1
			else:
				del stats['bots_later'][bot_day]
print(stats)
print(stats['plus'] * 30)
