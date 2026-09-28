package com.ruoyi.booth.controller;

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
import com.ruoyi.system.domain.DemoBooth;
import com.ruoyi.system.service.IDemoBoothService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 展位管理Controller
 * 
 * @author ruoyi
 * @date 2026-06-29
 */
@RestController
@RequestMapping("/booth/booth")
public class DemoBoothController extends BaseController
{
    @Autowired
    private IDemoBoothService demoBoothService;

    /**
     * 查询展位管理列表
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:list')")
    @GetMapping("/list")
    public TableDataInfo list(DemoBooth demoBooth)
    {
        startPage();
        List<DemoBooth> list = demoBoothService.selectDemoBoothList(demoBooth);
        return getDataTable(list);
    }

    /**
     * 导出展位管理列表
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:export')")
    @Log(title = "展位管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, DemoBooth demoBooth)
    {
        List<DemoBooth> list = demoBoothService.selectDemoBoothList(demoBooth);
        ExcelUtil<DemoBooth> util = new ExcelUtil<DemoBooth>(DemoBooth.class);
        util.exportExcel(response, list, "展位管理数据");
    }

    /**
     * 获取展位管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:query')")
    @GetMapping(value = "/{boothId}")
    public AjaxResult getInfo(@PathVariable("boothId") Long boothId)
    {
        return success(demoBoothService.selectDemoBoothByBoothId(boothId));
    }

    /**
     * 新增展位管理
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:add')")
    @Log(title = "展位管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody DemoBooth demoBooth)
    {
        return toAjax(demoBoothService.insertDemoBooth(demoBooth));
    }

    /**
     * 修改展位管理
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:edit')")
    @Log(title = "展位管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody DemoBooth demoBooth)
    {
        return toAjax(demoBoothService.updateDemoBooth(demoBooth));
    }

    /**
     * 删除展位管理
     */
    @PreAuthorize("@ss.hasPermi('booth:booth:remove')")
    @Log(title = "展位管理", businessType = BusinessType.DELETE)
    @DeleteMapping("/{boothIds}")
    public AjaxResult remove(@PathVariable Long[] boothIds)
    {
        return toAjax(demoBoothService.deleteDemoBoothByBoothIds(boothIds));
    }
}
