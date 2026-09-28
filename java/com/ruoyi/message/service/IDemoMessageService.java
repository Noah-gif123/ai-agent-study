package com.ruoyi.message.service;

import java.util.List;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.message.domain.DemoMessage;

/**
 * 申请消息管理Service接口
 * 
 * @author ruoyi
 * @date 2026-06-24
 */
public interface IDemoMessageService 
{
    /**
     * 查询申请消息管理
     * 
     * @param msgId 申请消息管理主键
     * @return 申请消息管理
     */
    public DemoMessage selectDemoMessageByMsgId(Long msgId);

    /**
     * 查询申请消息管理列表
     * 
     * @param demoMessage 申请消息管理
     * @return 申请消息管理集合
     */
    public List<DemoMessage> selectDemoMessageList(DemoMessage demoMessage);

    /**
     * 新增申请消息管理
     * 
     * @param demoMessage 申请消息管理
     * @return 结果
     */
    public int insertDemoMessage(DemoMessage demoMessage);

    /**
     * 修改申请消息管理
     * 
     * @param demoMessage 申请消息管理
     * @return 结果
     */
    public int updateDemoMessage(DemoMessage demoMessage);

    /**
     * 批量删除申请消息管理
     * 
     * @param msgIds 需要删除的申请消息管理主键集合
     * @return 结果
     */
    public int deleteDemoMessageByMsgIds(Long[] msgIds);

    /**
     * 删除申请消息管理信息
     * 
     * @param msgId 申请消息管理主键
     * @return 结果
     */
    public int deleteDemoMessageByMsgId(Long msgId);

    /**
     * 注册用户并更新申请消息
     * 
     * @param demoMessage 申请消息
     * @return 结果
     */
    public int regUserAndUpdateDemoMessage(DemoMessage demoMessage);

    /**
     * 校验用户名是否已提交过申请
     * 
     * @param user 用户
     * @return 结果
     */
    public boolean checkUserNameUnique(SysUser user);

    /**
     * 根据用户名查询申请消息
     * 
     * @param userName 用户名
     * @return 申请消息
     */
    public DemoMessage selectDemoMessageByUserName(String userName);
}
