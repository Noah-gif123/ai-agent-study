package com.ruoyi.message.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.message.domain.DemoMessage;
import com.ruoyi.message.service.IDemoMessageService;
import com.ruoyi.system.service.ISysUserService;

@Anonymous
@RestController
@RequestMapping("/api/message")
public class DemoMessageApiController extends BaseController{
	
	@Autowired
	private IDemoMessageService demoMessageService;
	
	@Autowired
	private ISysUserService userService;
	 
	/**
	 * 新增申请消息
	 */
	@PostMapping
	public AjaxResult add(@RequestBody DemoMessage demoMessage)
	{
		SysUser user = new SysUser();
		user.setUserName(demoMessage.getUserName());
		if (!userService.checkUserNameUnique(user)) {
	        return error("申请失败，此用户名已存在");
	    } else if(!demoMessageService.checkUserNameUnique(user)) {
	    	return error("此用户名已经发送过申请，请不要重复发送");
	    }
		return toAjax(demoMessageService.insertDemoMessage(demoMessage));
	}
}
