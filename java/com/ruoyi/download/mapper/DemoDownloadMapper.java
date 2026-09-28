package com.ruoyi.download.mapper;

import java.util.List;
import com.ruoyi.download.domain.DemoDownload;

/**
 * 资料下载管理Mapper接口
 * 
 * @author ruoyi
 * @date 2026-06-25
 */
public interface DemoDownloadMapper 
{
    /**
     * 查询资料下载管理
     * 
     * @param downId 资料下载管理主键
     * @return 资料下载管理
     */
    public DemoDownload selectDemoDownloadByDownId(Long downId);

    /**
     * 查询资料下载管理列表
     * 
     * @param demoDownload 资料下载管理
     * @return 资料下载管理集合
     */
    public List<DemoDownload> selectDemoDownloadList(DemoDownload demoDownload);

    /**
     * 新增资料下载管理
     * 
     * @param demoDownload 资料下载管理
     * @return 结果
     */
    public int insertDemoDownload(DemoDownload demoDownload);

    /**
     * 修改资料下载管理
     * 
     * @param demoDownload 资料下载管理
     * @return 结果
     */
    public int updateDemoDownload(DemoDownload demoDownload);

    /**
     * 删除资料下载管理
     * 
     * @param downId 资料下载管理主键
     * @return 结果
     */
    public int deleteDemoDownloadByDownId(Long downId);

    /**
     * 批量删除资料下载管理
     * 
     * @param downIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteDemoDownloadByDownIds(Long[] downIds);
}
