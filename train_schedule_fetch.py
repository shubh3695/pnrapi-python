import train_schedule

train = train_schedule.TrainSchedule("12906", "10", "2")#month and day are highly recommended
if train.request() == True:
    print train.get_json()
else:
    print train.error