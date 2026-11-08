"""作者：Wangyuan；日期：2026-10-29；职责：显式计数快照的增量与稳健异常分析。"""
import math
from statistics_core import modified_z_score

def run(payload):
    if not isinstance(payload,dict):raise TypeError('输入必须为对象')
    snapshots=payload.get('snapshots',[])
    if not isinstance(snapshots,list):raise TypeError('snapshots必须为数组')
    last={};history={};events=[];previous_time=None
    threshold=float(payload.get('z_threshold',3.5))
    if not math.isfinite(threshold) or threshold<=0:raise ValueError('阈值须为正数')
    for snap in snapshots:
        ts=float(snap['time']);values=snap['counts']
        if not math.isfinite(ts) or previous_time is not None and ts<=previous_time:raise ValueError('时间必须严格递增')
        if not isinstance(values,dict):raise TypeError('counts必须为对象')
        for ident,value in values.items():
            if not isinstance(value,int) or isinstance(value,bool) or value<0:raise ValueError('计数必须非负整数')
            if ident in last:
                delta=value-last[ident][1];dt=ts-last[ident][0]
                if not math.isfinite(dt) or dt<=0:raise ValueError('时间差必须有限且为正')
                hist=history.setdefault(ident,[])
                try:rate=delta*60/dt
                except OverflowError as exc:raise ValueError('计数变化超出可计算范围') from exc
                if not math.isfinite(rate):raise ValueError('变化速率必须有限')
                try:score=modified_z_score(rate,hist)
                except OverflowError as exc:raise ValueError('历史变化超出可计算范围') from exc
                if not math.isfinite(score):raise ValueError('异常得分必须有限')
                events.append({'id':ident,'time':ts,'delta':delta,'per_minute':rate,'reset':delta<0,'score':score,'anomaly':delta>=0 and abs(score)>=threshold})
                if delta>=0:hist.append(rate)
            last[ident]=(ts,value)
        previous_time=ts
    return {'events':events,'observed_ids':len(last),'notice':'异常只表示计数变化，需要来源复核；不判定作弊。'}
