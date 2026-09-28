package com.ruoyi.download.service.impl;

import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.download.mapper.DemoDownloadMapper;
import com.ruoyi.download.domain.DemoDownload;
import com.ruoyi.download.service.IDemoDownloadService;

/**
 * 资料下载管理Service业务层处理
 * 
 * @author ruoyi
 * @date 2026-06-25
 */
@Service
public class DemoDownloadServiceImpl implements IDemoDownloadService 
{
    @Autowired
    private DemoDownloadMapper demoDownloadMapper;

    /**
     * 查询资料下载管理
     * 
     * @param downId 资料下载管理主键
     * @return 资料下载管理
     */
    @Override
    public DemoDownload selectDemoDownloadByDownId(Long downId)
    {
        return demoDownloadMapper.selectDemoDownloadByDownId(downId);
    }

    /**
     * 查询资料下载管理列表
     * 
     * @param demoDownload 资料下载管理
     * @return 资料下载管理
     */
    @Override
    public List<DemoDownload> selectDemoDownloadList(DemoDownload demoDownload)
    {
        return demoDownloadMapper.selectDemoDownloadList(demoDownload);
    }

    /**
     * 新增资料下载管理
     * 
     * @param demoDownload 资料下载管理
     * @return 结果
     */
    @Override
    public int insertDemoDownload(DemoDownload demoDownload)
    {
        demoDownload.setCreateTime(DateUtils.getNowDate());
        return demoDownloadMapper.insertDemoDownload(demoDownload);
    }

    /**
     * 修改资料下载管理
     * 
     * @param demoDownload 资料下载管理
     * @return 结果
     */
    @Override
    public int updateDemoDownload(DemoDownload demoDownload)
    {
        demoDownload.setUpdateTime(DateUtils.getNowDate());
        return demoDownloadMapper.updateDemoDownload(demoDownload);
    }

    /**
     * 批量删除资料下载管理
     * 
     * @param downIds 需要删除的资料下载管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoDownloadByDownIds(Long[] downIds)
    {
        return demoDownloadMapper.deleteDemoDownloadByDownIds(downIds);
    }

    /**
     * 删除资料下载管理信息
     * 
     * @param downId 资料下载管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoDownloadByDownId(Long downId)
    {
        return demoDownloadMapper.deleteDemoDownloadByDownId(downId);
    }
}
