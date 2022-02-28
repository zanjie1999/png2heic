# coding=utf-8

# png2heic 批量图片转heic  gif转webp
# v2.2
# Sparkle 20220228
# 需要ffmpeg mp4box
# brew install ffmpeg mp4box
# apt-get install ffmpeg mp4box

import sys, os, uuid, shutil

# 输入图片目录
inPath = './'

# 输出图片目录
outPath = 'heic/'

# 是否把gif转webp
gif2webp = True

tmpFile = outPath + str( uuid.uuid4())[:8] + '.avc'

def covent(dir):
    print('Dir: ' + dir)
    l = os.listdir(dir)
    outDir = os.path.join(outPath,dir)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for i in l:
        inFile = os.path.join(dir,i)
        outName = None
        if os.path.isdir(inFile):
            covent(inFile)
        elif i.endswith('.jpg') or i.endswith('.png') or i.endswith('.JPG') or i.endswith('.PNG'):
            outName = i[:-3] + 'heic'
        elif i.endswith('.jpeg') or i.endswith('.JPEG'):
            outName = i[:-4] + 'heic'
        elif i.endswith('.gif') or i.endswith('.GIF'):
            if gif2webp:
                outDirName = os.path.join(outDir, i[:-3] + 'webp')
                if not os.path.exists(outDirName):
                    os.system('ffmpeg -i "' + inFile + '" -vcodec webp -loop 0 -deblock 1:1 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -pix_fmt yuva420p "' + outDirName + '"')
            else:
                outDirName = os.path.join(outDir, i[:-3] + 'gif')
                if not os.path.exists(outDirName):
                    shutil.copy(inFile, outDirName)
        if outName:
            outDirName = os.path.join(outDir,outName)
            if not os.path.exists(outDirName):
                print(inFile,' ',outDirName)
                os.system('ffmpeg -i "' + inFile + '" -crf 10 -psy-rd 0.4 -aq-strength 0.4 -deblock 1:1 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -preset veryslow -pix_fmt yuv444p10le -f hevc ' + tmpFile)
                os.system('mp4box -add-image ' + tmpFile + ' -ab heic -new "' + outDirName + '"')
                os.remove(tmpFile)
                # sys.exit(0)
    
    if os.listdir(outDir) == []:
        os.rmdir(outDir)


if not os.path.isdir(outPath):
    os.makedirs(outPath)

covent(inPath)