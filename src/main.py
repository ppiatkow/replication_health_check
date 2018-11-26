'''
Created on Nov 22, 2018

@author: kjnether

This is the script that:
  - initiates all the checks
  - creates and sends out the email.
'''
import ScheduleEvaluation
import DataUtil
import logging
import Constants
import Reporting

if __name__ == '__main__':
    # Settup logger
    formatStr = '%(asctime)s - %(lineno)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    #logging.basicConfig(level=logging.DEBUG)
    # formatStr = '[%(asctime)s] - %(name)s - {%(pathname)s:%(lineno)d} ' + \
    #            '%(levelname)s - %(message)s', datefmt
    logging.basicConfig(format=formatStr,
                        datefmt=datefmt,
                        level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # define what environment to work with
    env = 'PRD'

    emailReporter = Reporting.EmailStrings()

    # get the disabled schedules string
    dataUtil = DataUtil.GetData(env)
    scheds = dataUtil.getFMESchedules()
    schedsEval = ScheduleEvaluation.EvaluateSchedule(scheds)
    disabledSchedules = schedsEval.getDisabled()
    schedEvalStr = emailReporter.getDisableEmailStr(disabledSchedules)

    # getting fmw's in scheduled repo that don't have schedules
    scheduledRepoName = dataUtil.getMiscParam(Constants.SCHEDULE_REPO_LABEL)
    wrkSpcData = dataUtil.getFMWs(scheduledRepoName)
    notScheduled = schedsEval.compareRepositorySchedule(wrkSpcData)
    unschedFMWsStr = emailReporter.getUnsheduledRepoFMWsStr(notScheduled, scheduledRepoName)

    # schedules that reference data on the E: drive
    embedData = schedsEval.getEmbeddedData()
    embedDataEmailStr = emailReporter.getEmbeddedDataEmailStr(embedData)
    
    # now non prod or non OTHR replications
    nonProd = schedsEval.getNonProdSchedules()
    nonProdEmailStr = emailReporter.getNonProdSchedulesEmailStr(nonProd)
    logger.info('nonProd: %s', nonProd)
    print 'nonProd:', nonProd
    

    #detailedWrkSpcInfo = dataUtil.getScheduledFMWDetailInfo()
    
#     print 'unschedFMWsStr'
#     print unschedFMWsStr
#     # mta_acquired_tenure_history_sp_memprd_odb_bcgw.fmw
# 
#     print 'not scheduled:'
#     print '\n'.join(notScheduled)

#     for wrkspc in wrkSpcData:
#         print wrkspc.getWorkspaceName()
#         saveDate = wrkspc.getLastSaveDate()
#         print saveDate, type(saveDate)

    pass
