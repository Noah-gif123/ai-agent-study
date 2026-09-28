package com.ruoyi.download.controller;

import java.util.List;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.download.domain.DemoDownload;
import com.ruoyi.download.service.IDemoDownloadService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 资料下载管理Controller
 * 
 * @author ruoyi
 * @date 2026-06-25
 */
@RestController
@RequestMapping("/download/download")
public class DemoDownloadController extends BaseController
{
    @Autowired
    private IDemoDownloadService demoDownloadService;

    /**
     * 查询资料下载管理列表
     */
    @PreAuthorize("@ss.hasPermi('download:download:list')")
    @GetMapping("/list")
    public TableDataInfo list(DemoDownload demoDownload)
    {
        startPage();
        List<DemoDownload> list = demoDownloadService.selectDemoDownloadList(demoDownload);
        return getDataTable(list);
    }

    /**
     * 导出资料下载管理列表
     */
    @PreAuthorize("@ss.hasPermi('download:download:export')")
    @Log(title = "资料下载管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, DemoDownload demoDownload)
    {
        List<DemoDownload> list = demoDownloadService.selectDemoDownloadList(demoDownload);
        ExcelUtil<DemoDownload> util = new ExcelUtil<DemoDownload>(DemoDownload.class);
        util.exportExcel(response, list, "资料下载管理数据");
    }

    /**
     * 获取资料下载管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('download:download:query')")
    @GetMapping(value = "/{downId}")
    public AjaxResult getInfo(@PathVariable("downId") Long downId)
    {
        return success(demoDownloadService.selectDemoDownloadByDownId(downId));
    }

    /**
     * 新增资料下载管理
     */
    @PreAuthorize("@ss.hasPermi('download:download:add')")
    @Log(title = "资料下载管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody DemoDownload demoDownload)
    {
        return toAjax(demoDownloadService.insertDemoDownload(demoDownload));
    }

    /**
     * 修改资料下载管理
     */
    @PreAuthorize("@ss.hasPermi('download:download:edit')")
    @Log(title = "资料下载管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody DemoDownload demoDownload)
    {
        return toAjax(demoDownloadService.updateDemoDownload(demoDownload));
    }

    /**
     * 删除资料下载管理
     */
    @PreAuthorize("@ss.hasPermi('download:download:remove')")
    @Log(title = "资料下载管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{downIds}")
    public AjaxResult remove(@PathVariable Long[] downIds)
    {
        return toAjax(demoDownloadService.deleteDemoDownloadByDownIds(downIds));
    }
}
