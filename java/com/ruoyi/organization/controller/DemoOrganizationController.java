package com.ruoyi.organization.controller;

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
import com.ruoyi.organization.domain.DemoOrganization;
import com.ruoyi.organization.service.IDemoOrganizationService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 机构管理Controller
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
@RestController
@RequestMapping("/organization/organization")
public class DemoOrganizationController extends BaseController
{
    @Autowired
    private IDemoOrganizationService demoOrganizationService;

    /**
     * 查询机构管理列表
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:list')")
    @GetMapping("/list")
    public TableDataInfo list(DemoOrganization demoOrganization)
    {
        startPage();
        List<DemoOrganization> list = demoOrganizationService.selectDemoOrganizationList(demoOrganization);
        return getDataTable(list);
    }

    /**
     * 导出机构管理列表
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:export')")
    @Log(title = "机构管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, DemoOrganization demoOrganization)
    {
        List<DemoOrganization> list = demoOrganizationService.selectDemoOrganizationList(demoOrganization);
        ExcelUtil<DemoOrganization> util = new ExcelUtil<DemoOrganization>(DemoOrganization.class);
        util.exportExcel(response, list, "机构管理数据");
    }

    /**
     * 获取机构管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:query')")
    @GetMapping(value = "/{orgId}")
    public AjaxResult getInfo(@PathVariable("orgId") Long orgId)
    {
        return success(demoOrganizationService.selectDemoOrganizationByOrgId(orgId));
    }

    /**
     * 新增机构管理
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:add')")
    @Log(title = "机构管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody DemoOrganization demoOrganization)
    {
        return toAjax(demoOrganizationService.insertDemoOrganization(demoOrganization));
    }

    /**
     * 修改机构管理
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:edit')")
    @Log(title = "机构管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody DemoOrganization demoOrganization)
    {
        return toAjax(demoOrganizationService.updateDemoOrganization(demoOrganization));
    }

    /**
     * 删除机构管理
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:remove')")
    @Log(title = "机构管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{orgIds}")
    public AjaxResult remove(@PathVariable Long[] orgIds)
    {
        return toAjax(demoOrganizationService.deleteDemoOrganizationByOrgIds(orgIds));
    }

    /**
     * 查询机构管理列表（无分页）
     */
    @PreAuthorize("@ss.hasPermi('organization:organization:list')")
    @GetMapping("/listWithoutPage")
    public TableDataInfo listWithoutPage(DemoOrganization demoOrganization)
    {
        List<DemoOrganization> list = demoOrganizationService.selectDemoOrganizationList(demoOrganization);
        return getDataTable(list);
    }
}
