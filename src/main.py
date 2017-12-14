import git
import os

from pathlib import Path

from utils.temp import TemporaryDirectoryManager


def processIgnoreDirectory(sourceDir, ignoresToInclude):
    output = ''

    ignoreFilenames = [ignoreFile for ignoreFile in os.listdir(sourceDir) if ignoreFile.endswith('.gitignore')]

    for ignoreFilename in ignoreFilenames:
        if ignoreFilename.split('.')[0] in ignoresToInclude:
            output += '# Sourced from %s ignore file\n\n' % ignoreFilename

            with open(os.path.join(sourceDir, ignoreFilename), 'r') as ignoreFile:
               output += ignoreFile.read()

            output += '\n\n'

    return output


def getGitSource(outputPath, ignoresToInclude):
    """
    Download github global gitignore project, and place the code into the specified output folder

    :param outputPath: Location to copy gitignore source to
    """
    with TemporaryDirectoryManager(delete_files=True) as fileManager:
        # Initialise repo object and clone from the remote project
        gitRepo = git.Repo.init(path=fileManager.dir, bare=True)

        destinationDir = os.path.join(fileManager.dir, 'gitignore')

        gitRepo.clone_from('https://github.com/github/gitignore.git', destinationDir)

        finalIgnoreText = processIgnoreDirectory(destinationDir, ignoresToInclude)
        finalIgnoreText += processIgnoreDirectory(os.path.join(destinationDir, 'Global'), ignoresToInclude)

    with open(outputPath, 'w') as outputFile:
        outputFile.write(finalIgnoreText)


def main():
    getGitSource(os.path.join(Path.home(), '.gitignore'),
                 ['Python', 'Go', 'Rust', 'Scala', 'JetBrains', 'Windows', 'Linux'])


if __name__ == '__main__':
    main()
