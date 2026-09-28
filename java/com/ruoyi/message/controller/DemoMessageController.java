package com.ruoyi.message.controller;

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
import com.ruoyi.message.domain.DemoMessage;
import com.ruoyi.message.service.IDemoMessageService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.system.service.ISysUserService;
import com.ruoyi.web.controller.common.Const;

/**
 * 申请消息管理Controller
 * 
 * @author ruoyi
 * @date 2026-06-24
 */
@RestController
@RequestMapping("/message/message")
public class DemoMessageController extends BaseController
{
    @Autowired
    private IDemoMessageService demoMessageService;

    @Autowired
    private ISysUserService userService;

    /**
     * 查询申请消息管理列表
     */
    @PreAuthorize("@ss.hasPermi('message:message:list')")
    @GetMapping("/list")
    public TableDataInfo list(DemoMessage demoMessage)
    {
        String userRoleGroup = userService.selectUserRoleGroup(SecurityUtils.getUsername());
        if(StringUtils.isNotNull(userRoleGroup) && userRoleGroup.equals(Const.ORGUSER_ROLE_NAME)) {
            demoMessage.setUserId(SecurityUtils.getUserId());
        }
        startPage();
        List<DemoMessage> list = demoMessageService.selectDemoMessageList(demoMessage);
        return getDataTable(list);
    }

    /**
     * 导出申请消息管理列表
     */
    @PreAuthorize("@ss.hasPermi('message:message:export')")
    @Log(title = "申请消息管理", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, DemoMessage demoMessage)
    {
        List<DemoMessage> list = demoMessageService.selectDemoMessageList(demoMessage);
        ExcelUtil<DemoMessage> util = new ExcelUtil<DemoMessage>(DemoMessage.class);
        util.exportExcel(response, list, "申请消息管理数据");
    }

    /**
     * 获取申请消息管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('message:message:query')")
    @GetMapping(value = "/{msgId}")
    public AjaxResult getInfo(@PathVariable("msgId") Long msgId)
    {
        return success(demoMessageService.selectDemoMessageByMsgId(msgId));
    }

    /**
     * 新增申请消息管理
     */
    @PreAuthorize("@ss.hasPermi('message:message:add')")
    @Log(title = "申请消息管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody DemoMessage demoMessage)
    {
        return toAjax(demoMessageService.insertDemoMessage(demoMessage));
    }

    /**
     * 修改申请消息管理
     */
    @PreAuthorize("@ss.hasPermi('message:message:edit')")
    @Log(title = "申请消息管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody DemoMessage demoMessage)
    {
        return toAjax(demoMessageService.updateDemoMessage(demoMessage));
    }

    /**
     * 删除申请消息管理
     */
    @PreAuthorize("@ss.hasPermi('message:message:remove')")
    @Log(title = "申请消息管理", businessType = BusinessType.DELETE)
    @DeleteMapping("/{msgIds}")
    public AjaxResult remove(@PathVariable Long[] msgIds)
    {
        return toAjax(demoMessageService.deleteDemoMessageByMsgIds(msgIds));
    }

    /**
     * 審核通過or不通過申请消息
     */
    @PreAuthorize("@ss.hasPermi('message:message:audit')")
    @Log(title = "申请消息", businessType = BusinessType.UPDATE)
    @PutMapping("/isApprove")
    public AjaxResult isApprove(@RequestBody DemoMessage demoMessage)
    {    
        String status = demoMessage.getMsgUnapprovedReason() == null || "".equals(demoMessage.getMsgUnapprovedReason()) ? Const.MSG_STATUS_APPROVED : Const.MSG_STATUS_UNAPPROVED;
        demoMessage.setMsgStatus(status);
        demoMessage.setMsgApprovedUserId(this.getUserId());
        demoMessage.setMsgApprovedTime(DateUtils.getNowDate());
        int i = demoMessageService.regUserAndUpdateDemoMessage(demoMessage);
        if (i > 0) {
            return AjaxResult.success();
        } else if (i == -1) {
            return AjaxResult.error("注册新用户失败");
        } else if (i == -2) {
            return AjaxResult.error("审核前，请先在'系统管理-角色管理'中添加名为'机构用户'的角色，并授予申请消息查询和查看详情、云场景提交审核、云服务提交审核等权限");
        } else {
            return AjaxResult.error("审核操作失败");
        }
    }
}
