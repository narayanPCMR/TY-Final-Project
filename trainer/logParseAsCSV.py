LOGFILE = "output/log_default_settings.log"
OUT_ACCR_CSV = "output/acceptanceRatio_table.csv"
OUT_TRAIN_CSV = "output/training_table.csv"

with open(LOGFILE) as f:
    a = f.readlines()
    
    trainingStage = 0
    acR_csv = "Training Stage,Acceptance Ratio"
    stage_start = False
    stages = []
    stage_text = ''
    
    for l in a:
        if "<BEGIN" in l:
            stage_start = True
        if "END>" in l:
            stages.append(stage_text)
            stage_text = ''
            stage_start = False
        
        if stage_start:
            stage_text += l
        
        if "NEG count : acceptanceRatio" in l:
            d = l.split('    ')
            d = d[-1].split(':')
            d = [x.strip() for x in d]
            acceptanceRatio = d[-1]
            acR_csv += '\n{},{}'.format(trainingStage, acceptanceRatio)
            trainingStage += 1
    
    #Last stage
    #Get the table of HR and FA
    training_step_csv = "Training Step,Hit Rate,False Alarm Rate"
    last_stage = stages[-1]
    last_stage = last_stage.split('\n')
    for x in range(7, len(last_stage), 2):
        d = last_stage[x].split('|')
        d = [x.strip() for x in d if x.strip() is not ""]
        training_step_csv += '\n' + ','.join(d)
    
    with open(OUT_ACCR_CSV, "w") as g:
        g.write(acR_csv)
    with open(OUT_TRAIN_CSV, "w") as g:
        g.write(training_step_csv)