#!/usr/bin/python
import time

import sys

from AbbyyOnlineSdk import *

processor = AbbyyOnlineSdk()  # work wih Abbyy Cloud OCR SDK


# Recognize a file at filePath and save result to resultFilePath
def recognize_file(file_path, result_file_path, output_format):
    print "Uploading.."
    settings = ProcessingSettings()
    settings.OutputFormat = output_format
    task = processor.ProcessImage(file_path, settings)

    """
    if task == None:
        print "Error"
        return
    print "Id = %s" % task.Id
    print "Status = %s" % task.Status

    # Wait for the task to be completed
    sys.stdout.write( "Waiting.." )
    # Note: it's recommended that your application waits at least 2 seconds
    # before making the first getTaskStatus request and also between such requests
    # for the same task. Making requests more often will not improve your
    # application performance.
    # Note: if your application queues several files and waits for them
    # it's recommended that you use listFinishedTasks instead (which is described
    # at http://ocrsdk.com/documentation/apireference/listFinishedTasks/).
    """

    while task.IsActive():
        time.sleep(5)
        sys.stdout.write(".")
        task = processor.GetTaskStatus(task)

    if task.Status == "Completed":
        processor.DownloadResult(task, result_file_path)
        """if task.DownloadUrl != None:
            processor.DownloadResult( task, resultFilePath )
            print "Result was written to %s" % resultFilePath
            """
    else:
        print "Error processing task"
