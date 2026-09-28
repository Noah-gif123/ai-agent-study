package com.ruoyi.message.mapper;

import java.util.List;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import com.ruoyi.common.core.domain.entity.SysUser;
import com.ruoyi.message.domain.DemoMessage;

import org.apache.ibatis.annotations.Mapper;

/**
 * 申请消息管理Mapper接口
 * 
 * @author ruoyi
 * @date 2026-06-24
 */
@Mapper
public interface DemoMessageMapper 
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
     * 删除申请消息管理
     * 
     * @param msgId 申请消息管理主键
     * @return 结果
     */
    public int deleteDemoMessageByMsgId(Long msgId);

    /**
     * 批量删除申请消息管理
     * 
     * @param msgIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteDemoMessageByMsgIds(Long[] msgIds);

    /**
     * 校验用户名是否已提交过申请
     * 
     * @param user 用户
     * @return 结果
     */
    public DemoMessage selectDemoMessageByUserName(
            @NotBlank(message = "用户账号不能为空") @Size(min = 0, max = 30, message = "用户账号长度不能超过30个字符") String userName);

    /**
     * 校验用户名是否已提交过申请
     * 
     * @param user 用户
     * @return 结果
     */
    public DemoMessage checkUserNameUnique(SysUser user);
}
