import datetime
import os
import subprocess
import logging

logging.basicConfig(
    filename='nfs-backup-logs.txt',
    format='%(asctime)s %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    level=logging.INFO
)


class S3Backup:
    def __init__(self, bucket_location, local_location):
        self._bucket = bucket_location
        self._local_location = local_location

    def _start_sync_subprocess(self, input_location, output_location, delete=False, exclude=None):
        """Start a s3 sync, optionally passing the delete flag and excluding specified files"""
        cmd = ['aws', 's3', 'sync', input_location, output_location]
        if delete:
            cmd.append('--delete')
        if exclude is not None:
            cmd += ['--exclude', exclude]
        subprocess.call(cmd)

    def cleanup(self):
        """
        Delete backups for the previous month
        """
        try:
            now = datetime.datetime.now()
            year = now.year if now.month > 1 else now.year - 1
            month = now.month - 1 if now.month > 1 else 12
            logging.info('Cleaning up: {}-{}*'.format(year, month))
            cmd = ['aws', 's3', 'rm', 's3://{}/'.format(self._bucket), '--recursive', '--exclude', '*', '--include', '{}-{}*'.format(year, month)]
            subprocess.call(cmd)
        except Exception as e:
            logging.info('Failed cleanup')
            logging.info(e)


    def backup(self):
        """
        Sync the configured drive to a configured s3 location under a 'year-month' folder
        """
        try:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
            day = now.day
            logging.info('Backing up to: {}-{}-{}'.format(year, month, day))
            s3_location = 's3://{}/{}-{}-{}'.format(self._bucket, year, month, day)
            self._start_sync_subprocess(self._local_location, s3_location)
        except Exception as e:
            logging.info('Failed backup')
            logging.info(e)


if __name__ == '__main__':
    logging.info('Starting back up process')
    bucket = os.environ.get('S3_NFS_BACKUP_BUCKET')
    backuper = S3Backup(bucket, 'D:\\')
    backuper.backup()
    logging.info('Starting cleanup process')
    backuper.cleanup()
