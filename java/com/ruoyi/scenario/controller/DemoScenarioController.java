package com.ruoyi.scenario.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.message.domain.DemoMessage;
import com.ruoyi.web.controller.common.Const;
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
import com.ruoyi.scenario.domain.DemoScenario;
import com.ruoyi.scenario.service.IDemoScenarioService;
import com.ruoyi.system.service.ISysUserService;
import com.ruoyi.message.service.IDemoMessageService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 云场景Controller
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
@RestController
@RequestMapping("/scenario/scenario")
public class DemoScenarioController extends BaseController
{
    @Autowired
    private IDemoScenarioService demoScenarioService;

    @Autowired
    private ISysUserService userService;

    @Autowired
    private IDemoMessageService demoMessageService;

    /**
     * 查询云场景列表
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:list')")
    @GetMapping("/list")
    public TableDataInfo list(DemoScenario demoScenario)
    {
        String userRoleGroup = userService.selectUserRoleGroup(this.getUsername());
        if(StringUtils.isNotNull(userRoleGroup) && userRoleGroup.equals(Const.ORGUSER_ROLE_NAME)) {
            DemoMessage demoMessage = demoMessageService.selectDemoMessageByUserName(this.getUsername());
            if (demoMessage == null || demoMessage.getOrgId() == null) {
                return getDataTable(java.util.Collections.emptyList());
            }
            demoScenario.setOrgId(demoMessage.getOrgId());
        }
        startPage();
        List<DemoScenario> list = demoScenarioService.selectDemoScenarioList(demoScenario);
        return getDataTable(list);
    }

    /**
     * 导出云场景列表
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:export')")
    @Log(title = "云场景", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, DemoScenario demoScenario)
    {
        List<DemoScenario> list = demoScenarioService.selectDemoScenarioList(demoScenario);
        ExcelUtil<DemoScenario> util = new ExcelUtil<DemoScenario>(DemoScenario.class);
        util.exportExcel(response, list, "云场景数据");
    }

    /**
     * 获取云场景详细信息
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:query')")
    @GetMapping(value = "/{sceId}")
    public AjaxResult getInfo(@PathVariable("sceId") Long sceId)
    {
        return success(demoScenarioService.selectDemoScenarioBySceId(sceId));
    }

    /**
     * 新增云场景
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:add')")
    @Log(title = "云场景", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody DemoScenario demoScenario)
    {
        demoScenario.setCreateUserId(getUserId());
        return toAjax(demoScenarioService.insertDemoScenario(demoScenario));
    }

    /**
     * 修改云场景
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:edit')")
    @Log(title = "云场景", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody DemoScenario demoScenario)
    {
        return toAjax(demoScenarioService.updateDemoScenario(demoScenario));
    }

    /**
     * 删除云场景
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:remove')")
    @Log(title = "云场景", businessType = BusinessType.DELETE)
	@DeleteMapping("/{sceIds}")
    public AjaxResult remove(@PathVariable Long[] sceIds)
    {
        return toAjax(demoScenarioService.deleteDemoScenarioBySceIds(sceIds));
    }

    /**
     * 審核通過or不通過云场景
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:audit')")
    @Log(title = "云场景", businessType = BusinessType.UPDATE)
    @PutMapping("/isApprove")
    public AjaxResult isApprove(@RequestBody DemoScenario demoScenario)
    {
        Map<String,Object> params = new HashMap<String,Object>();
        Long[] ids=new Long[]{demoScenario.getSceId()};
        params.put("ids", ids);
        String status=demoScenario.getSceUnapprovedReason()==null||"".equals(demoScenario.getSceUnapprovedReason())?Const.SCE_STATUS_OPEN: Const.SCE_STATUS_UNAPPROVED;
        params.put("sceStatus", status);
        params.put("sceApprovedUserId", this.getUserId());
        params.put("sceApprovedTime", DateUtils.getNowDate());
        params.put("sceUnApprovedReason", demoScenario.getSceUnapprovedReason());

        int i = demoScenarioService.updateScenarioByIds(params);
        if(i>0){
            return AjaxResult.success();
        }else{
            return AjaxResult.error("当前状态是"+(demoScenario.getSceStatus()==null?"空":demoScenario.getSceStatus())+"，无法进行审核操作");
        }
    }

    /**
     * 批量審核通過云场景
     */
    @PreAuthorize("@ss.hasPermi('scenario:scenario:passApprove')")
    @Log(title = "云场景", businessType = BusinessType.UPDATE)
    @PutMapping("/passApprove/{ids}")
    public AjaxResult passApprove(@PathVariable Long[] ids)
    {
        Map<String,Object> params = new HashMap<String,Object>();
        params.put("ids", ids);
        params.put("sceStatus", Const.SCE_STATUS_OPEN);
        params.put("approvedByUserId", this.getUserId());
        params.put("approvedTime", DateUtils.getNowDate());
        params.put("action", "APPROVE");
        int i = demoScenarioService.updateScenarioByIds(params);
        if(i>0){
            return AjaxResult.success();
        }else{
            return AjaxResult.error("只有状态为‘审核中’的云场景才能进行审核操作");
        }
    }

    @PreAuthorize("@ss.hasPermi('scenario:scenario:approve')")
    @Log(title = "云场景", businessType = BusinessType.UPDATE)
    @PutMapping("/approve/{ids}")
    public AjaxResult approve(@PathVariable Long[] ids)
    {
        Map<String,Object> params = new HashMap<String,Object>();
        params.put("ids", ids);
        params.put("sceStatus", Const.SCE_STATUS_SUBMITTED);
        params.put("createUserId",this.getUserId());
        params.put("updateTime",DateUtils.getNowDate());
        params.put("action", "SUBMIT");
        System.out.println("params:"+params);
        int i = demoScenarioService.updateScenarioByIds(params);
        if(i>0){
            return AjaxResult.success();
        }else{
            return AjaxResult.error("只有状态为‘布展中’的云场景才能进行提交审核操作");
        }
    }
}
