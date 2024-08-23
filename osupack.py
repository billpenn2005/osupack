import cmd2
import sys
import argparse
import os
import shutil
import zipfile

def merge_name(song_name=str(),creator=str()):
    return song_name+' ['+creator+']'

def get_songs(song_path):
    return os.listdir(song_path)

def get_modified_beatmap_str(lines,cntr=int(),song_name=str(),creator=str(),pic=str(),aud=str(),pak=str()):
    #lines=file.readlines()
    new_name=merge_name(song_name,creator)
    pack_name=pak
    ret=str()
    md=0
    for i in lines:
        if i.find('AudioFilename')!=-1:
            ret+='AudioFilename:'+str(cntr)+'.'+aud.split('.')[-1]+'\n'
        elif i.find('TitleUnicode')!=-1:
            ret+='TitleUnicode:'+pack_name+'\n'
        elif i.find('Title')!=-1:
            ret+='Title:'+pack_name+'\n'
        elif i.find('ArtistUnicode')!=-1:
            ret+='ArtistUnicode:'+'Various Artists'+'\n'
        elif i.find('Artist')!=-1:
            ret+='Artist:'+'Various Artists'+'\n'
        elif i.find('Version')!=-1:
            ret+='Version:'+new_name+'\n'
        elif i.find('BeatmapID')!=-1:
            ret+='BeatmapID:0\n'
        elif i.find('BeatmapSetID')!=-1:
            ret+='BeatmapSetID:-1\n'
        elif md==0:
            if i.find('[Events]')!=-1:
                ret+='[Events]\n'
                md=1
                continue
            else:
                ret+=i
        else:
            if i[:2]=='//':
                continue
            else:
                isp=i.strip('\n')
                isplit=isp.split(',')
                ret+=isplit[0]+','+isplit[1]+',"'+str(cntr)+'.'+pic.split('.')[-1]+'",'+isplit[3]+','+isplit[4]+'\n'
                md=0
    return ret

def get_pic_name(lines):
    #lines=file.readlines()
    md=0
    for i in lines:
        #print(i)
        if md==0:
            if i.find('[Events]')!=-1:
                md=1
                continue
        else:
            if i[:2]=='//':
                continue
            else:
                #print(i)
                isp=i.strip('\n')
                isplit=isp.split(',')
                return isplit[2].strip('"')

def get_audio_name(lines):
    #lines=file.readlines()
    for i in lines:
        if i.find('AudioFilename')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_song_name(lines):
    for i in lines:
        if i.find('TitleUnicode')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_creator(lines):
    for i in lines:
        if i.find('Creator')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')
 
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


class Packer(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.folderpath=str()
        self.add_settable(cmd2.Settable('folderpath',str,'folder to pack',self))
        self.packname=str()
        self.add_settable(cmd2.Settable('packname',str,'name of pack',self))
        self.creator=str()
        self.add_settable(cmd2.Settable('creator',str,'name of creator',self))
    run_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(run_parser)
    def do_run(self,args):
        self.poutput('running')
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        song_list=get_songs(self.folderpath)
        song_path=self.folderpath
        cntr=1
        if not os.path.exists(self.folderpath+'//delete'):
            os.mkdir(self.folderpath+'//delete')
        shutil.copy('0.osu',self.folderpath+'//delete//0.osu')
        for i in song_list:
            father_path=song_path+'//'+i
            lst=os.listdir(father_path)
            for j in lst:
                spl=j.split('.')
                if spl[-1]=='osu':
                    osu_file_name=father_path+'//'+j
                    osu_file=open(osu_file_name,encoding='utf-8')
                    lns=osu_file.readlines()
                    song_name=get_song_name(lns)
                    creator=get_creator(lns)
                    pic_name=get_pic_name(lns)
                    audio_name=get_audio_name(lns)
                    outfile_str=get_modified_beatmap_str(lns,cntr,song_name,creator,pic_name,audio_name,self.packname)
                    osu_file.close()
                    #self.poutput(pic_name)
                    #osu_file=open('tmp//'+str(cntr)+'.osu')
                    #osu_file.write(outfile_str)
                    #osu_file.close()
                    with open('tmp//Various Artists - '+self.packname+' ('+self.creator+') '+'['+merge_name(song_name,creator)+']'+'.osu', mode="w", encoding="utf-8") as f:
                        f.write(outfile_str)
                    if os.path.exists(father_path+'//'+pic_name):
                        shutil.copy(father_path+'//'+pic_name,'tmp//'+str(cntr)+'.'+pic_name.split('.')[-1])
                    if os.path.exists(father_path+'//'+audio_name):
                        shutil.copy(father_path+'//'+audio_name,'tmp//'+str(cntr)+'.'+audio_name.split('.')[-1])
                    cntr+=1
        zipDir('tmp',self.packname+'.osz')
        shutil.rmtree('tmp')
        self.poutput('finished')

if __name__=='__main__':
    packer=Packer()
    sys.exit(packer.cmdloop())