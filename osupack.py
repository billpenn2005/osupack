import sys
import argparse
import os
import shutil
import zipfile

def merge_name(song_name=str(),creator=str()):
    return song_name+' ['+creator+']'

def get_songs(song_path):
    return os.listdir(song_path)

def get_new_name(song_name,creator,diff_name,ispack,isperson_pack):
    if (not ispack) and (not isperson_pack):
        new_name=merge_name(song_name,creator)
    elif ispack:
        new_name=diff_name
    elif isperson_pack:
        new_name=merge_name(diff_name,creator)
    return new_name

def get_modified_beatmap_str(lines,cntr=int(),song_name=str(),creator=str(),pic=str(),aud=str(),pak=str(),tags=str(),pack_creator=str(),snu=str(),diff_name=str(),ispack=False,isperson_pack=False):
    #print(song_name)
    new_name=get_new_name(song_name,creator,diff_name,ispack,isperson_pack)
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
        elif i.find('Tags')!=-1:
            ret+='Tags:'+tags+'\n'
        elif i.find('Creator')!=-1:
            ret+='Creator:'+pack_creator+'\n'
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
    md=0
    for i in lines:
        if md==0:
            if i.find('[Events]')!=-1:
                md=1
                continue
        else:
            if i[:2]=='//':
                continue
            else:
                isp=i.strip('\n')
                isplit=isp.split(',')
                return isplit[2].strip('"')

def get_audio_name(lines):
    for i in lines:
        if i.find('AudioFilename')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_song_name_unicode(lines):
    for i in lines:
        if i.find('TitleUnicode')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()
        
def get_song_name(lines):
    for i in lines:
        if i.find('Title')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_creator(lines):
    for i in lines:
        if i.find('Creator')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_tags(lines):
    for i in lines:
        if i.find('Tags')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()
        
def get_BeatmapID(lines):
    for i in lines:
        if i.find('BeatmapID')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()
        
def get_BeatmapSetID(lines):
    for i in lines:
        if i.find('BeatmapSetID')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def get_diffname(lines):
    for i in lines:
        if i.find('Version')!=-1:
            isp=i.strip('\n')
            isplit=isp.split(':')
            return isplit[-1].strip()

def zipDir(dirpath, outFullName):
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def pack_songs(folderpath, packname, creator, extratags=''):
    print('running')
    bbcode_file=open('bbcode.txt','a', encoding='utf-8')
    bbcode_file.write('[box=map list]\n')
    link_template='https://osu.ppy.sh/beatmapsets/{}#mania/{}'
    song_hyperlink_template='[url={}]{}[/url]'
    mapper_link_template='https://osu.ppy.sh/users/{}'
    mapper_hyperlink_template='[url={}]{}[/url]'
    if(extratags is None):
        extratags=''
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    song_list=get_songs(folderpath)
    song_path=folderpath
    cntr=1
    if not os.path.exists(folderpath+'//delete'):
        os.mkdir(folderpath+'//delete')
    shutil.copy(resource_path('0.osu'),folderpath+'//delete//0.osu')
    all_tags=extratags
    pack_mp={}
    person_pack_mp={}
    for i in song_list:
        father_path=song_path+'//'+i
        lst=os.listdir(father_path)
        pack_mp[i]=False
        person_pack_mp[i]=False
        for j in lst:
            spl=j.split('.')
            if spl[-1]=='osu':
                osu_file_name=father_path+'//'+j
                osu_file=open(osu_file_name,encoding='utf-8')
                lns=osu_file.readlines()
                all_tags+=get_tags(lns)+' '
                osu_file.close()
            elif spl[-1]=='PACK':
                pack_mp[i]=True
            elif spl[-1]=='P_PACK':
                person_pack_mp[i]=True
    with open('tags.txt','w', encoding='utf-8') as f:
        f.write(all_tags)
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
                snu=get_song_name_unicode(lns)
                creator_=get_creator(lns)
                pic_name=get_pic_name(lns)
                audio_name=get_audio_name(lns)
                bm_id=get_BeatmapID(lns)
                bms_id=get_BeatmapSetID(lns)
                diffname=get_diffname(lns)
                bbcode_file.write(song_hyperlink_template.format(link_template.format(bms_id,bm_id),song_name)+' by '+mapper_hyperlink_template.format(mapper_link_template.format(creator_),creator_)+'\n')
                outfile_str=get_modified_beatmap_str(lns,cntr,song_name,creator_,pic_name,audio_name,packname,all_tags,creator,snu,diffname,pack_mp[i],person_pack_mp[i])
                osu_file.close()
                new_name=get_new_name(song_name,creator_,diffname,pack_mp[i],person_pack_mp[i])
                with open('tmp//Various Artists - '+packname+' ('+creator+') '+'['+new_name+']'+'.osu', mode="w", encoding="utf-8") as f:
                    f.write(outfile_str)
                if os.path.exists(father_path+'//'+pic_name):
                    shutil.copy(father_path+'//'+pic_name,'tmp//'+str(cntr)+'.'+pic_name.split('.')[-1])
                if os.path.exists(father_path+'//'+audio_name):
                    shutil.copy(father_path+'//'+audio_name,'tmp//'+str(cntr)+'.'+audio_name.split('.')[-1])
                cntr+=1
    zipDir('tmp',packname+'.osz')
    shutil.rmtree('tmp')
    bbcode_file.write('[/box]\n')
    bbcode_file.close()
    print('finished')

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OSU Beatmap Packer')
    parser.add_argument('--dir', type=str, required=True, help='folder to pack')
    parser.add_argument('--packname', type=str, required=True, help='name of pack')
    parser.add_argument('--creator', type=str, required=True, help='name of creator')
    parser.add_argument('--extratags', type=str, required=False, help='extra tags')

    args = parser.parse_args()
    
    pack_songs(args.dir, args.packname, args.creator,args.extratags)