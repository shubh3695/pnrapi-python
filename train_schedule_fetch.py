import train_schedule

train = train_schedule.TrainSchedule("12906","10","4", "56")
if train.request() == True:
    print train.get_json()
else:
    print train.error