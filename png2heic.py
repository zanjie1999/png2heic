# coding=utf-8

# png2heic 批量图片转heic  gif转webp
# v6.0
# Sparkle 20220228
# 需要ffmpeg mp4box exiftool
# Windows：ffmpeg(https://www.gyan.dev/ffmpeg/builds) gpac(https://gpac.io/downloads) exiftool(https://exiftool.org/index.html)
# macOS：brew install ffmpeg mp4box exiftool
# Linus：apt-get install ffmpeg mp4box exiftool

import os, sys, uuid, shutil

# 输入输出图片目录配置 可以配置多个目录，左输入，右输出 Win需要将\改成/
inPathOutPath = {
    'Genshin Impact Game/ScreenShot/': '游戏截图/原神/',
    'StarRail Game/StarRail_Data/ScreenShots/': '游戏截图/星铁/',
    'ZenlessZoneZero Game/ScreenShot/': '游戏截图/绝区零/',
    'D:\Pictures\Screenshots': 'D:\Pictures\Screenshots',
}

# 在输出目录创建一个输入文件夹名的文件夹（方便多个输入输出到同一个目录）
makeInDirInOutDir = False

# 是否把gif转webp
gif2webp = False

# 是否复制exif信息
copyExif = False

# 使用yuv444 10bit Android不兼容 颜色会好一丁点
useYuv444 = False

# 转换heic 可以将不支持的heic转换成目标heic
coventHeic = False

# 删除原文件
deleteInFile = False

# 三个依赖的执行文件路径，如果已加入PATH那就维持这样就好
ffmpeg = 'ffmpeg'
mp4box = 'mp4box'
exiftool = 'exiftool'

# ffmpeg公共参数，可以修改增加更多自定义功能
# 例如在vf中增加滤镜，用半角逗号,来分隔多个效果，默认的scale调整大小是为了将分辨率转成2的倍数（因为heic不支持）,你也可以修改他来调整输出分辨率
# 举个例子，从左上角裁剪 crop=WIDTH:HEIGHT:X:Y 可以让你在多显示器截图时只保存留显示器1的部分，那就修改成 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,crop=3840:2160:0:0"
ffmpegArg = '-deblock 1:1 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '


ffmpegArgHevc = ffmpegArg + '-crf 10 -psy-rd 0.4 -aq-strength 0.4 -preset veryslow -pix_fmt ' + ('yuv444p10le' if useYuv444 else 'yuv420p10le')

# 临时文件存在当前目录
tmpFile = os.path.dirname(os.path.abspath(__file__)) + '/' + str( uuid.uuid4())[:8] + '.hvc'
if getattr(sys, 'frozen', False):
    tmpFile = os.path.dirname(sys.executable) + '/' + str( uuid.uuid4())[:8] + '.hvc'

def exec(cmd):
    print(cmd)
    os.system(cmd)

def covent(dir, inPath, outPath, outDirJoinDirName):
    print('Dir: ' + dir)
    l = os.listdir(dir)
    l = sorted(l, key=lambda x: os.path.getctime(os.path.join(dir, x)))
    outDir = outPath
    if outDirJoinDirName:
        outDir = os.path.join(outPath,dir)
    elif dir != inPath:
        outDir = os.path.join(outPath,dir[len(inPath):])
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for i in l:
        inFile = os.path.join(dir,i)
        outName = None
        outDirName = None
        if os.path.isdir(inFile):
            covent(inFile, inPath, outPath, outDirJoinDirName)
        elif i.endswith('.jpg') or i.endswith('.png') or i.endswith('.JPG') or i.endswith('.PNG'):
            outName = i[:-3] + 'heic'
        elif i.endswith('.jpeg') or i.endswith('.JPEG'):
            outName = i[:-4] + 'heic'
        elif i.endswith('.gif') or i.endswith('.GIF'):
            if gif2webp:
                outDirName = os.path.join(outDir, i[:-3] + 'webp')
                if not os.path.exists(outDirName):
                    print(inFile,' ',outDirName)
                    exec(f'{ffmpeg} -i "{inFile}" -vcodec webp -loop 0 {ffmpegArg} -pix_fmt yuva420p "{outDirName}"')
                    if copyExif:
                        exec(f'{exiftool} -tagsFromFile "{inFile}" -overwrite_original "{outDirName}"')
            else:
                outDirName = os.path.join(outDir, i[:-3] + 'gif')
                if not os.path.exists(outDirName):
                    # 不转换gif就复制gif过去
                    print(inFile,' ',outDirName)
                    shutil.copy(inFile, outDirName)
        elif i.endswith('.HEIC') or i.endswith('.heic'):
            outDirName = os.path.join(outDir, i[:-4] + 'heic')
            if coventHeic:
                if not os.path.exists(outDirName):
                    print(inFile,' ',outDirName)
                    exec(f'{mp4box} -dump-item 1:path={tmpFile}.hvc1 "{inFile}"')
                    exec(f'{ffmpeg} -i {tmpFile}.hvc1 {ffmpegArgHevc} -f hevc ' + tmpFile)
                    exec(f'{mp4box} -add-image {tmpFile}:primary -ab heic -new "{outDirName}"')
                    os.remove(tmpFile + '.hvc1')
                    os.remove(tmpFile)
                    if copyExif:
                        exec(f'{exiftool} -tagsFromFile "{inFile}" -overwrite_original "{outDirName}"')
            elif not os.path.exists(outDirName):
                # 不转换heic不存在就复制过去
                print(inFile,' ',outDirName)
                shutil.copy(inFile, outDirName)
        if outName:
            outDirName = os.path.join(outDir,outName)
            if not os.path.exists(outDirName):
                print(inFile,' ',outDirName)
                exec(f'{ffmpeg} -i "{inFile}" {ffmpegArgHevc} -f hevc ' + tmpFile)
                exec(f'{mp4box} -add-image {tmpFile}:primary -ab heic -new "{outDirName}"')
                os.remove(tmpFile)
                if copyExif:
                    exec(f'{exiftool} -tagsFromFile "{inFile}" -overwrite_original "{outDirName}"')
                
        if outDirName:
            s = os.stat(inFile) # 同步 访问时间 修改时间
            os.utime(outDirName, (s.st_atime, s.st_mtime))

        # 确保输出文件正常再删除
        if deleteInFile and outDirName and os.path.getsize(outDirName) > 1:
            os.remove(inFile)
    
    if os.listdir(outDir) == []:
        os.rmdir(outDir)


if __name__ == "__main__":
    for inPath, outPath in inPathOutPath.items():
        if inPath[-1] != '/':
            inPath += '/'
        if outPath[-1] != '/':
            outPath += '/'
        if not os.path.isdir(outPath):
            os.makedirs(outPath)
        covent(inPath, inPath, outPath, makeInDirInOutDir)
