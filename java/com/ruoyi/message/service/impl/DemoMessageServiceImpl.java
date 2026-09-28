package com.ruoyi.message.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ruoyi.common.constant.UserConstants;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.message.mapper.DemoMessageMapper;
import com.ruoyi.message.domain.DemoMessage;
import com.ruoyi.message.service.IDemoMessageService;
import com.ruoyi.common.core.domain.entity.SysRole;
import com.ruoyi.system.service.ISysRoleService;
import com.ruoyi.system.service.ISysUserService;
import com.ruoyi.web.controller.common.Const;

/**
 * 申请消息管理Service业务层处理
 * 
 * @author ruoyi
 * @date 2026-06-24
 */
@Service
public class DemoMessageServiceImpl implements IDemoMessageService 
{
    @Autowired
    private DemoMessageMapper demoMessageMapper;

    @Autowired
    private ISysUserService userService;

    @Autowired
    private ISysRoleService roleService;

    /**
     * 查询申请消息管理
     * 
     * @param msgId 申请消息管理主键
     * @return 申请消息管理
     */
    @Override
    public DemoMessage selectDemoMessageByMsgId(Long msgId)
    {
        return demoMessageMapper.selectDemoMessageByMsgId(msgId);
    }

    /**
     * 查询申请消息管理列表
     * 
     * @param demoMessage 申请消息管理
     * @return 申请消息管理
     */
    @Override
    public List<DemoMessage> selectDemoMessageList(DemoMessage demoMessage)
    {
        return demoMessageMapper.selectDemoMessageList(demoMessage);
    }

    /**
     * 新增申请消息管理
     * 
     * @param demoMessage 申请消息管理
     * @return 结果
     */
    @Override
    public int insertDemoMessage(DemoMessage demoMessage)
    {
        return demoMessageMapper.insertDemoMessage(demoMessage);
    }

    /**
     * 修改申请消息管理
     * 
     * @param demoMessage 申请消息管理
     * @return 结果
     */
    @Override
    public int updateDemoMessage(DemoMessage demoMessage)
    {
        return demoMessageMapper.updateDemoMessage(demoMessage);
    }

    /**
     * 批量删除申请消息管理
     * 
     * @param msgIds 需要删除的申请消息管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoMessageByMsgIds(Long[] msgIds)
    {
        return demoMessageMapper.deleteDemoMessageByMsgIds(msgIds);
    }

    /**
     * 删除申请消息管理信息
     * 
     * @param msgId 申请消息管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoMessageByMsgId(Long msgId)
    {
        return demoMessageMapper.deleteDemoMessageByMsgId(msgId);
    }

    @Transactional(rollbackFor = Exception.class)
    @Override
    public int regUserAndUpdateDemoMessage(DemoMessage demoMessage) {
        // TODO Auto-generated method stub
        if (Const.MSG_STATUS_APPROVED.equals(demoMessage.getMsgStatus())) {
            // 审核通过，添加用户，分配用户权限
            SysUser user = new SysUser();
            user.setUserName(demoMessage.getUserName());
            user.setNickName(demoMessage.getNickName());
            user.setEmail(demoMessage.getEmail());
            user.setPhonenumber(demoMessage.getPhonenumber());
            user.setPassword(SecurityUtils.encryptPassword(Const.ORIGIN_PASSWORD));
            user.setCreateBy(SecurityUtils.getUsername());
            if (userService.registerUser(user)) {
                // 查询名为"机构用户"的角色的ID
                SysRole sysRole = new SysRole();
                sysRole.setRoleName(Const.ORGUSER_ROLE_NAME.toString());
                List<SysRole> roleList = roleService.selectRoleList(sysRole);
                // System.out.println("roleList:::::::::::" + roleList);
                if (roleList == null || roleList.size() == 0) {
                    return -2; // 不存在"机构用户"角色
                }
                Long[] roleIds = new Long[] { roleList.get(0).getRoleId() };
                // 为用户授权"机构用户"角色
                userService.insertUserAuth(user.getUserId(), roleIds);
                demoMessage.setUserId(user.getUserId());
            } else {
                return -1;
            }
        }
        return demoMessageMapper.updateDemoMessage(demoMessage);
    }

	@Override
	public boolean checkUserNameUnique(SysUser user) {
		// TODO Auto-generated method stub
		DemoMessage info = demoMessageMapper.selectDemoMessageByUserName(user.getUserName());
        if (StringUtils.isNotNull(info))
        {
            return UserConstants.NOT_UNIQUE;
        }
        return UserConstants.UNIQUE;
	}

	@Override
	public DemoMessage selectDemoMessageByUserName(String username) {
		// TODO Auto-generated method stub
		return demoMessageMapper.selectDemoMessageByUserName(username);
	}
}
